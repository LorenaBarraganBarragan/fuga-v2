"""
test_leaks.py — Pruebas de endpoints de detección de fugas (HU-23, HU-24, F8)
"""

import uuid
from app.api.v1.leaks import get_leaks
from app.core.security import CurrentUser


def test_get_leaks_sin_gastos():
    uid = uuid.uuid4()
    user = CurrentUser(user_id=uid, email="test@fuga.plus", rol="usuario")
    res = get_leaks(user=user)

    assert res.estado == "sin_gastos"
    assert res.total == 0
    assert "aún no tienes gastos" in res.mensaje_d15.lower()
