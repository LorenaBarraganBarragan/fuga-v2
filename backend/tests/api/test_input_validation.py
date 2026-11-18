from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.expenses import ExpenseCreate


@pytest.mark.parametrize("value", [None, 123, True, {"texto": "taxi"}])
def test_non_string_interpretation_is_422_not_500(private_client, value):
    result = private_client.post("/api/v1/expenses/interpret", json={"texto": value})
    assert result.status_code == 422
    assert result.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.parametrize("fecha", [1763164800, "2026-01-01T00:00:00"])
def test_confirmed_date_rejects_timestamp_coercion(fecha):
    with pytest.raises(ValidationError):
        ExpenseCreate(monto_cop=8000, descripcion="taxi", categoria_id=uuid4(), fecha_gasto=fecha)


def test_client_cannot_invent_interpretation_version():
    with pytest.raises(ValidationError):
        ExpenseCreate(
            monto_cop=8000,
            descripcion="taxi",
            categoria_id=uuid4(),
            fecha_gasto="2026-01-01",
            diccionario_version="99",
        )
