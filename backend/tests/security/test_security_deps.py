"""
test_security_deps.py — Pruebas de seguridad transversal y dependencia de token (F2)
"""

import uuid
import pytest
import jwt

from app.core.security import get_current_user
from app.core.errors import UnauthenticatedException, AccountDisabledException


def test_sin_token_devuelve_401():
    with pytest.raises(UnauthenticatedException) as exc_info:
        get_current_user(authorization=None)
    assert exc_info.value.code == "UNAUTHENTICATED"


def test_formato_invalido_devuelve_401():
    with pytest.raises(UnauthenticatedException) as exc_info:
        get_current_user(authorization="Basic 123456")
    assert exc_info.value.code == "UNAUTHENTICATED"


def test_token_sin_sub_devuelve_401():
    token = jwt.encode({"email": "test@fuga.plus"}, "secret", algorithm="HS256")
    with pytest.raises(UnauthenticatedException) as exc_info:
        get_current_user(authorization=f"Bearer {token}")
    assert exc_info.value.code == "UNAUTHENTICATED"


def test_usuario_deshabilitado_devuelve_403():
    uid = str(uuid.uuid4())
    token = jwt.encode(
        {"sub": uid, "disabled_at": "2026-11-15T00:00:00Z"},
        "secret",
        algorithm="HS256",
    )
    with pytest.raises(AccountDisabledException) as exc_info:
        get_current_user(authorization=f"Bearer {token}")
    assert exc_info.value.code == "ACCOUNT_DISABLED"


def test_token_valido_obtiene_usuario():
    uid = str(uuid.uuid4())
    token = jwt.encode(
        {"sub": uid, "email": "test@fuga.plus", "user_metadata": {"rol": "usuario"}},
        "secret",
        algorithm="HS256",
    )
    user = get_current_user(authorization=f"Bearer {token}")
    assert str(user.user_id) == uid
    assert user.email == "test@fuga.plus"
    assert user.rol == "usuario"
