"""
test_interpret.py — Pruebas del endpoint de interpretación de gastos (F5)
"""

import uuid
import pytest

from app.api.v1.expenses import interpret_expense
from app.core.security import CurrentUser
from app.schemas.expenses import InterpretRequest


def _usuario_valido() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), email="test@fuga.plus", rol="usuario")


def test_interpret_endpoint_exitoso():
    user = _usuario_valido()
    req = InterpretRequest(texto="Hoy gasté $8.000 en un taxi")
    res = interpret_expense(request=req, user=user)

    assert "draft" in res
    assert res["draft"]["monto_cop"] == 8000
    assert res["draft"]["categoria_nombre"] == "Transporte"
    assert "confianza" in res
    assert "avisos" in res
    assert "ambiguedades" in res
    assert res["diccionario_version"] == "1.0"
    assert res["reglas_version"] == "1.0"


def test_interpret_endpoint_longitud_excedida():
    with pytest.raises(Exception):
        InterpretRequest(texto="a" * 281)


def test_interpret_endpoint_texto_vacio():
    with pytest.raises(Exception):
        InterpretRequest(texto="   ")
