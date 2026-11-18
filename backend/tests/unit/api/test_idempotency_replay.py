import hashlib
import json
from datetime import date, datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

from app.repositories.expenses import ExpensesRepository
from app.schemas.expenses import ExpenseCreate, ExpenseResponse


def test_retry_returns_original_response_after_edit_or_soft_delete():
    uid = uuid4()
    key = uuid4()
    category = uuid4()
    now = datetime.now(timezone.utc)
    body = ExpenseCreate(
        monto_cop=8000, descripcion="taxi", fecha_gasto=date(2026, 1, 1), categoria_id=category
    )
    original = ExpenseResponse(
        id=uuid4(),
        usuario_id=uid,
        categoria_id=category,
        monto_cop=8000,
        descripcion="taxi",
        fecha_gasto=date(2026, 1, 1),
        moneda="COP",
        diccionario_version="1.0",
        reglas_version="1.0",
        clave_idempotencia=key,
        created_at=now,
        updated_at=now,
    )
    row = original.model_dump()
    row.update(
        monto_cop=9000,
        deleted_at=now,
        idempotency_response=original.model_dump(mode="json"),
        request_hash=hashlib.sha256(
            json.dumps(
                body.model_dump(mode="json", exclude={"texto_original"}), sort_keys=True
            ).encode()
        ).hexdigest(),
    )
    result = SimpleNamespace(mappings=lambda: SimpleNamespace(first=lambda: row))
    db = SimpleNamespace(execute=lambda *a, **kw: result)
    replay, status = ExpensesRepository(uid).create(db, body, key)
    assert status == 200
    assert replay.id == original.id
    assert replay.monto_cop == 8000
    assert replay.deleted_at is None
