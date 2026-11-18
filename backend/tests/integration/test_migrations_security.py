"""SQL real contra PostgreSQL desechable, con defaults permisivos como Supabase."""

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, ProgrammingError

pytestmark = pytest.mark.integration
ROOT = Path(__file__).resolve().parents[3]


def account(db):
    uid = uuid4()
    db.execute(
        text("INSERT INTO auth.users(id,email) VALUES (:id,:email)"),
        {"id": uid, "email": str(uid) + "@local.invalid"},
    )
    return uid


def expense(db, uid, amount=8000, when=None):
    cid = db.execute(text("SELECT id FROM public.categoria WHERE nombre='Transporte'")).scalar_one()
    gid = uuid4()
    db.execute(
        text("""INSERT INTO public.gasto
      (id,usuario_id,categoria_id,monto_cop,descripcion,fecha_gasto,diccionario_version,reglas_version,clave_idempotencia)
      VALUES (:id,:uid,:cat,:amount,'taxi',:date,'1.0','1.0',:key)"""),
        {
            "id": gid,
            "uid": uid,
            "cat": cid,
            "amount": amount,
            "date": when or date(2026, 1, 1),
            "key": uuid4(),
        },
    )
    return gid, cid


def authenticated(db, uid):
    db.execute(text("SET LOCAL ROLE authenticated"))
    db.execute(
        text("SELECT set_config('request.jwt.claims',:claims,true)"),
        {"claims": json.dumps({"sub": str(uid), "role": "authenticated"})},
    )


def test_rls_two_users_and_column_permissions(database):
    a, b = account(database), account(database)
    expense(database, a)
    expense(database, b)
    authenticated(database, a)
    assert database.execute(text("SELECT id FROM public.perfil")).scalars().all() == [a]
    database.execute(text("UPDATE public.perfil SET nombres='Usuario A' WHERE id=:id"), {"id": a})
    assert (
        database.execute(
            text("SELECT nombres FROM public.perfil WHERE id=:id"), {"id": a}
        ).scalar_one()
        == "Usuario A"
    )
    assert (
        database.execute(
            text("UPDATE public.perfil SET nombres='Intruso' WHERE id=:id"), {"id": b}
        ).rowcount
        == 0
    )
    assert database.execute(text("SELECT count(*) FROM public.gasto")).scalar_one() == 0
    assert database.execute(text("SELECT count(*) FROM public.fuga")).scalar_one() == 0
    assert database.execute(text("SELECT count(*) FROM public.fuga_evidencia")).scalar_one() == 0
    for statement in [
        "UPDATE public.perfil SET rol='administrador'",
        "UPDATE public.perfil SET disabled_at=now()",
        "UPDATE public.perfil SET auth_sync_pendiente=true",
        "UPDATE public.perfil SET foto_url='https://invalid.test'",
        "TRUNCATE public.gasto",
        "DELETE FROM public.gasto",
    ]:
        with pytest.raises(ProgrammingError), database.begin_nested():
            database.execute(text(statement))
    database.execute(
        text("SELECT set_config('request.jwt.claims',:claims,true)"),
        {"claims": json.dumps({"sub": str(b)})},
    )
    assert database.execute(text("SELECT id FROM public.perfil")).scalars().all() == [b]


def test_catalogues_read_only_and_anon_denied(database):
    uid = account(database)
    authenticated(database, uid)
    assert database.execute(text("SELECT count(*) FROM public.categoria")).scalar_one() == 9
    assert not database.execute(
        text("SELECT has_schema_privilege('authenticated','public','CREATE')")
    ).scalar_one()
    for statement in [
        "UPDATE public.categoria SET nombre='Otra'",
        "DELETE FROM public.categoria",
        "TRUNCATE public.categoria",
        "UPDATE public.regla_fuga_version SET parametros='{}'",
    ]:
        with pytest.raises(ProgrammingError), database.begin_nested():
            database.execute(text(statement))
    database.execute(text("SET LOCAL ROLE anon"))
    for statement in [
        "SELECT * FROM public.categoria",
        "SELECT * FROM public.perfil",
        "SELECT * FROM public.auditoria",
    ]:
        with pytest.raises(ProgrammingError), database.begin_nested():
            database.execute(text(statement))


def test_auth_trigger_runs_as_provider_ignores_role_metadata(database):
    uid = uuid4()
    database.execute(text("SET LOCAL ROLE supabase_auth_admin"))
    database.execute(
        text(
            "INSERT INTO auth.users(id,email,raw_user_meta_data) VALUES (:id,'auth@local.invalid',CAST(:meta AS jsonb))"
        ),
        {"id": uid, "meta": json.dumps({"rol": "administrador"})},
    )
    database.execute(text("RESET ROLE"))
    row = database.execute(
        text("SELECT rol,nombres,apellido FROM public.perfil WHERE id=:id"), {"id": uid}
    ).one()
    assert tuple(row) == ("usuario", None, None)


def test_auth_users_existing_before_migrations_have_profile(database):
    row = database.execute(
        text(
            "SELECT p.rol FROM public.perfil p JOIN auth.users u ON u.id=p.id WHERE u.email='preexisting@local.invalid'"
        )
    ).one()
    assert row[0] == "usuario"


def test_constraints_and_evidence_owner(database):
    a, b = account(database), account(database)
    ga, cid = expense(database, a)
    gb, _ = expense(database, b)
    rv = database.execute(
        text("SELECT id FROM public.regla_fuga_version WHERE version='1.0'")
    ).scalar_one()
    fid = uuid4()
    database.execute(
        text("""INSERT INTO public.fuga(id,usuario_id,regla_version_id,categoria_id,descripcion_normalizada,
      ocurrencias,monto_acumulado_cop,fecha_desde,fecha_hasta) VALUES (:id,:uid,:rv,:cat,'taxi',3,24000,'2026-01-01','2026-01-03')"""),
        {"id": fid, "uid": a, "rv": rv, "cat": cid},
    )
    with pytest.raises(IntegrityError), database.begin_nested():
        database.execute(
            text("INSERT INTO public.fuga_evidencia(fuga_id,gasto_id) VALUES (:f,:g)"),
            {"f": fid, "g": gb},
        )
    database.execute(
        text("INSERT INTO public.fuga_evidencia(fuga_id,gasto_id) VALUES (:f,:g)"),
        {"f": fid, "g": ga},
    )
    for sql, params in [
        ("UPDATE public.gasto SET usuario_id=:b WHERE id=:g", {"b": b, "g": ga}),
        ("UPDATE public.fuga SET usuario_id=:b WHERE id=:f", {"b": b, "f": fid}),
        ("UPDATE public.perfil SET nombres=' ' WHERE id=:a", {"a": a}),
        ("INSERT INTO public.categoria(nombre,orden) VALUES ('Inventada',10)", {}),
    ]:
        with pytest.raises(IntegrityError), database.begin_nested():
            database.execute(text(sql), params)
    for amount in (0, -1, 100_000_001):
        with pytest.raises(IntegrityError), database.begin_nested():
            expense(database, a, amount)
    tomorrow = datetime.now(ZoneInfo("America/Bogota")).date() + timedelta(days=1)
    with pytest.raises(IntegrityError), database.begin_nested():
        expense(database, a, when=tomorrow)


def test_reapply_and_seed_preserve_existing_data(postgres_engine, database):
    uid = account(database)
    database.execute(text("UPDATE public.perfil SET nombres='Conservar' WHERE id=:id"), {"id": uid})
    gid, _ = expense(database, uid)
    database.commit()
    before = database.execute(
        text("SELECT monto_cop,clave_idempotencia FROM public.gasto WHERE id=:id"), {"id": gid}
    ).one()
    database.rollback()  # Release SELECT locks before testing DDL on another connection.
    with postgres_engine.begin() as conn:
        conn.exec_driver_sql("SET LOCAL lock_timeout='5s'")
        conn.exec_driver_sql("SET LOCAL search_path=pg_catalog")
        for path in sorted((ROOT / "supabase/migrations").glob("*.sql")):
            conn.exec_driver_sql(path.read_text(encoding="utf-8-sig"))
        conn.exec_driver_sql((ROOT / "supabase/seed.sql").read_text(encoding="utf-8-sig"))
    assert (
        database.execute(
            text("SELECT nombres FROM public.perfil WHERE id=:id"), {"id": uid}
        ).scalar_one()
        == "Conservar"
    )
    assert (
        database.execute(
            text("SELECT monto_cop,clave_idempotencia FROM public.gasto WHERE id=:id"), {"id": gid}
        ).one()
        == before
    )
    assert database.execute(text("SELECT count(*) FROM public.categoria")).scalar_one() == 9


def test_read_only_sql_verification(postgres_engine):
    raw = postgres_engine.raw_connection()
    original_autocommit = raw.driver_connection.autocommit
    try:
        raw.driver_connection.autocommit = True
        raw.driver_connection.execute(
            (ROOT / "supabase/tests/verificar_esquema.sql").read_text(encoding="utf-8")
        )
    finally:
        raw.driver_connection.autocommit = original_autocommit
        raw.close()


def test_catalogue_matches_canonical_dictionary(database):
    from app.domain.expenses.diccionario_v1 import CATEGORIAS

    expected = [(c["nombre"], c["orden"]) for c in CATEGORIAS.values()]
    rows = database.execute(text("SELECT nombre,orden FROM public.categoria ORDER BY orden")).all()
    assert [tuple(r) for r in rows] == expected


def test_disabled_account_cannot_read_or_update_profile_directly(database):
    uid = account(database)
    database.execute(text("UPDATE public.perfil SET disabled_at=now() WHERE id=:id"), {"id": uid})
    authenticated(database, uid)
    assert database.execute(text("SELECT count(*) FROM public.perfil")).scalar_one() == 0
    assert (
        database.execute(
            text("UPDATE public.perfil SET nombres='Cambio' WHERE id=:id"), {"id": uid}
        ).rowcount
        == 0
    )


def test_rule_versions_are_immutable(database):
    with pytest.raises(IntegrityError), database.begin_nested():
        database.execute(text("UPDATE public.regla_fuga_version SET parametros='{}'"))
