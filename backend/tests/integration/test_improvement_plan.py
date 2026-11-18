"""Regression and query budgets, exclusively on the disposable local database."""

from datetime import datetime, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import event, text

from app.services.analytics_service import AnalyticsService
from app.services.leaks_service import LeaksService

pytestmark = pytest.mark.integration


def coffee_account(db):
    uid = uuid4()
    db.execute(
        text("INSERT INTO auth.users(id,email) VALUES (:id,'coffee@local.invalid')"), {"id": uid}
    )
    category = db.execute(text("SELECT id FROM categoria WHERE nombre='Alimentación'")).scalar_one()
    today = datetime.now(ZoneInfo("America/Bogota")).date()
    for offset, description in ((4, "gaste cafe"), (3, "cafe"), (1, "cafe"), (0, "por cafe")):
        db.execute(
            text("""INSERT INTO gasto
          (id,usuario_id,categoria_id,monto_cop,descripcion,fecha_gasto,
           diccionario_version,reglas_version,clave_idempotencia)
          VALUES (:id,:uid,:cat,5000,:description,:date,'1.0','1.0',:key)"""),
            {
                "id": uuid4(),
                "uid": uid,
                "cat": category,
                "description": description,
                "date": today - timedelta(days=offset),
                "key": uuid4(),
            },
        )
    db.commit()
    return uid


def test_repeated_analysis_does_not_write_unchanged_snapshots(database, postgres_engine):
    uid = coffee_account(database)
    first = LeaksService.detect_leaks(uid, database)
    assert first.items[0].monto_acumulado_cop == 20000
    statements = []

    def record(conn, cursor, statement, parameters, context, executemany):
        statements.append(statement.strip())

    event.listen(postgres_engine, "before_cursor_execute", record)
    try:
        second = LeaksService.detect_leaks(uid, database)
    finally:
        event.remove(postgres_engine, "before_cursor_execute", record)
    writes = [s for s in statements if s.startswith(("UPDATE fuga", "INSERT INTO fuga"))]
    assert second == first
    assert writes == [], f"Unchanged analysis performed {len(writes)} snapshot writes"


def test_snapshot_tracks_updated_evidence_and_normalization_version(database, monkeypatch):
    uid = coffee_account(database)
    first = LeaksService.detect_leaks(uid, database)
    monkeypatch.setattr("app.services.leaks_service.NORMALIZACION_VERSION", "future-test-version")
    changed = LeaksService.detect_leaks(uid, database)
    assert changed.items[0].id != first.items[0].id
    assert changed.items[0].monto_acumulado_cop == 20000
    assert (
        database.execute(
            text("SELECT count(*) FROM fuga WHERE usuario_id=:uid AND vigente"), {"uid": uid}
        ).scalar_one()
        == 1
    )
    assert (
        database.execute(
            text("SELECT count(*) FROM gasto WHERE usuario_id=:uid"), {"uid": uid}
        ).scalar_one()
        == 4
    )


def test_monthly_sql_aggregation_reduces_rows_and_preserves_counts(database):
    uid = coffee_account(database)
    period = datetime.now(ZoneInfo("America/Bogota")).strftime("%Y-%m")
    rows = AnalyticsService.rows(uid, period, database)
    # Only dates in the selected month count, including around month boundaries.
    today = datetime.now(ZoneInfo("America/Bogota")).date()
    count = sum((today - timedelta(days=i)).month == today.month for i in (4, 3, 1, 0))
    assert len(rows) == 1
    assert int(rows[0]["cantidad"]) == count
    summary = AnalyticsService.get_summary(uid, period, database)
    assert summary.monto_total_cop == count * 5000
    assert summary.cantidad_gastos == count
    assert summary.promedio_gasto_cop == 5000
    breakdown = AnalyticsService.get_by_category(uid, period, database)
    assert breakdown.categorias_mayor_gasto == ["Alimentación"]
    coffee = next(item for item in breakdown.items if item.categoria_nombre == "Alimentación")
    assert (coffee.cantidad, coffee.monto_cop, coffee.porcentaje) == (count, count * 5000, 100.0)


def test_expired_window_invalidates_snapshot_without_changing_expenses(database, monkeypatch):
    uid = coffee_account(database)
    first = LeaksService.detect_leaks(uid, database)
    today = datetime.now(ZoneInfo("America/Bogota"))

    class Later(datetime):
        @classmethod
        def now(cls, tz=None):
            return (today + timedelta(days=31)).astimezone(tz)

    monkeypatch.setattr("app.services.leaks_service.datetime", Later)
    assert LeaksService.detect_leaks(uid, database).total == 0
    assert (
        database.execute(
            text("SELECT vigente FROM fuga WHERE id=:id"), {"id": first.items[0].id}
        ).scalar_one()
        is False
    )
    assert (
        database.execute(
            text("SELECT count(*) FROM gasto WHERE usuario_id=:uid"), {"uid": uid}
        ).scalar_one()
        == 4
    )


def test_concurrent_analysis_keeps_one_current_snapshot(database, postgres_engine):
    from concurrent.futures import ThreadPoolExecutor

    from sqlalchemy.orm import Session

    uid = coffee_account(database)

    def analyze(_):
        with Session(postgres_engine) as session:
            return LeaksService.detect_leaks(uid, session).items[0].id

    with ThreadPoolExecutor(max_workers=2) as pool:
        ids = list(pool.map(analyze, range(2)))
    assert ids[0] == ids[1]
    assert (
        database.execute(
            text("SELECT count(*) FROM fuga WHERE usuario_id=:uid AND vigente"), {"uid": uid}
        ).scalar_one()
        == 1
    )


def test_retention_queue_reactivation_and_restrictive_audit_foreign_key(database, monkeypatch):
    import httpx
    from sqlalchemy.exc import IntegrityError

    from app.core.config import settings
    from app.services.accounts_service import change_state

    uid = coffee_account(database)
    monkeypatch.setattr(settings, "SUPABASE_SERVICE_ROLE_KEY", "sb_secret_local_fixture")
    monkeypatch.setattr(
        "app.services.accounts_service.httpx.put",
        lambda *a, **kw: httpx.Response(
            200, request=httpx.Request("PUT", "https://provider.example.test"), json={}
        ),
    )
    change_state(uid, False, uid, database, allow_self=True)
    row = database.execute(
        text(
            "SELECT p.disabled_at,t.suprimir_desde,t.estado FROM perfil p "
            "JOIN tarea_retencion t ON t.usuario_id=p.id WHERE p.id=:id"
        ),
        {"id": uid},
    ).one()
    assert row[1] - row[0] == timedelta(days=30)
    assert row[2] == "pendiente"
    change_state(uid, True, uid, database, allow_self=True)
    assert (
        database.execute(
            text("SELECT estado FROM tarea_retencion WHERE usuario_id=:id"), {"id": uid}
        ).scalar_one()
        == "cancelada"
    )
    # Proves why an operator cannot blindly cascade-delete a profile with audit/history.
    with pytest.raises(IntegrityError), database.begin_nested():
        database.execute(text("DELETE FROM perfil WHERE id=:id"), {"id": uid})
    assert (
        database.execute(
            text("SELECT count(*) FROM gasto WHERE usuario_id=:id"), {"id": uid}
        ).scalar_one()
        == 4
    )
