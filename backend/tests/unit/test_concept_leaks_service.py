"""Servicio real con persistencia simulada: historial inmutable y snapshots versionados."""

import hashlib
import json
from copy import deepcopy
from datetime import UTC, date, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.domain.expenses.diccionario_v1 import NORMALIZACION_VERSION
from app.domain.leaks.rule_fuga_01 import PARAMETROS_DEFAULT_V1_0
from app.services.leaks_service import LeaksService


class FrozenDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 11, 18, 17, tzinfo=UTC).astimezone(tz)


def test_service_reads_legacy_descriptions_and_uses_new_snapshot_fingerprint(monkeypatch):
    category = str(uuid4())
    expenses = [
        {
            "id": str(uuid4()),
            "categoria_id": category,
            "descripcion": description,
            "monto_cop": 5000,
            "fecha_gasto": date(2026, 11, day),
            "deleted_at": None,
        }
        for day, description in ((14, "gaste cafe"), (15, "cafe"), (17, "cafe"), (18, "por cafe"))
    ]
    original = deepcopy(expenses)
    rule_id = uuid4()
    statements = []
    snapshots = []
    evidence_ids = []
    commits = []

    def execute(statement, parameters=None):
        sql = str(statement)
        statements.append(sql)
        if "SELECT v.id,v.version,v.parametros" in sql:
            row = {"id": rule_id, "version": "1.0", "parametros": PARAMETROS_DEFAULT_V1_0}
            return SimpleNamespace(mappings=lambda: SimpleNamespace(first=lambda: row))
        if "SELECT id,categoria_id,monto_cop,descripcion,fecha_gasto,deleted_at" in sql:
            return SimpleNamespace(mappings=lambda: SimpleNamespace(all=lambda: expenses))
        if "SELECT id FROM fuga" in sql:
            return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: []))
        if "SELECT id,vigente FROM fuga" in sql:
            return SimpleNamespace(first=lambda: None)
        if "INSERT INTO fuga\n" in sql:
            snapshots.append(dict(parameters))
        if "INSERT INTO fuga_evidencia" in sql:
            evidence_ids.extend(parameters["gids"])
        if "SELECT id,nombre FROM categoria" in sql:
            return SimpleNamespace(all=lambda: [(category, "Alimentación")])
        return None

    monkeypatch.setattr("app.services.leaks_service.datetime", FrozenDateTime)
    database = SimpleNamespace(execute=execute, commit=lambda: commits.append(True))
    result = LeaksService.detect_leaks(uuid4(), database)
    assert result.estado == "candidatos"
    assert result.total == 1
    assert result.items[0].descripcion_normalizada == "cafe"
    assert result.items[0].ocurrencias == 4
    assert result.items[0].monto_acumulado_cop == 20000
    assert result.items[0].regla_version == "1.0"
    assert set(evidence_ids) == {row["id"] for row in expenses}
    expected = hashlib.sha256(
        json.dumps(
            {"normalizacion_version": NORMALIZACION_VERSION, "gastos": expenses},
            sort_keys=True,
            default=str,
        ).encode()
    ).hexdigest()
    assert len(snapshots) == 1
    assert snapshots[0]["hash"] == expected
    assert commits == [True]
    assert expenses == original
    assert not any(
        sql.lstrip().startswith(("UPDATE gasto", "INSERT INTO gasto", "DELETE FROM gasto"))
        for sql in statements
    )


@pytest.mark.parametrize("version", ["1.0", "1.1"])
def test_http_draft_and_confirmation_accept_current_and_legacy_versions(
    private_client, monkeypatch, version
):
    from app.repositories.categories import CATALOGO_ESTATICO
    from app.schemas.expenses import ExpenseResponse

    monkeypatch.setattr(
        "app.repositories.categories.CategoriesRepository.list_all",
        lambda self, db: CATALOGO_ESTATICO,
    )
    interpreted = private_client.post(
        "/api/v1/expenses/interpret", json={"texto": "Hoy compré café por 5000"}
    )
    assert interpreted.status_code == 200
    draft = interpreted.json()
    assert draft["draft"]["descripcion"] == "cafe"
    assert (draft["diccionario_version"], draft["reglas_version"]) == ("1.1", "1.1")
    confirmed = {
        key: draft["draft"][key] for key in ("monto_cop", "categoria_id", "fecha_gasto", "moneda")
    }
    # Manual correction remains a human description, never overwritten by canonicalization.
    confirmed.update(
        descripcion="Mi café del barrio", diccionario_version=version, reglas_version=version
    )
    received = []

    def create(user_id, body, key, db):
        received.append(body)
        now = datetime.now(UTC)
        return ExpenseResponse(
            **body.model_dump(),
            id=uuid4(),
            usuario_id=user_id,
            clave_idempotencia=key,
            created_at=now,
            updated_at=now,
        ), 201

    monkeypatch.setattr("app.services.expenses_service.ExpensesService.create_expense", create)
    response = private_client.post(
        "/api/v1/expenses", json=confirmed, headers={"Idempotency-Key": str(uuid4())}
    )
    assert response.status_code == 201
    assert response.json()["descripcion"] == "Mi café del barrio"
    assert received[0].diccionario_version == version
