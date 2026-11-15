"""
test_expenses_endpoint.py — Pruebas unitarias de las funciones de endpoint (F5)
Invoca las funciones del router directamente sin sockets HTTP.
"""

import uuid
import pytest
from app.api.v1.expenses import interpret_expense
from app.core.security import CurrentUser
from app.schemas.expenses import InterpretRequest
from app.core.errors import ValidationException


def test_interpret_expense_directo():
    user = CurrentUser(user_id=uuid.uuid4(), email="test@fuga.plus")
    req = InterpretRequest(texto="Hoy gasté $8.000 en un taxi")
    res = interpret_expense(request=req, user=user)

    assert "draft" in res
    assert res["draft"]["monto_cop"] == 8000
    assert res["draft"]["categoria_nombre"] == "Transporte"
    assert res["confianza"]["monto"] == "alta"
    assert res["diccionario_version"] == "1.0"


def test_interpret_expense_texto_vacio_pydantic():
    with pytest.raises(Exception):
        InterpretRequest(texto="")


def test_interpret_expense_longitud_excedida_pydantic():
    with pytest.raises(Exception):
        InterpretRequest(texto="a" * 281)
