"""
test_security.py — Pruebas unitarias de decodificación de tokens y seguridad (F2)
"""

import uuid
import pytest
import jwt
from app.core.security import decode_token, CurrentUser
from app.core.errors import UnauthenticatedException, AccountDisabledException


def test_decode_token_valido():
    uid = str(uuid.uuid4())
    token = jwt.encode({"sub": uid, "email": "test@fuga.plus"}, "secret", algorithm="HS256")
    payload = decode_token(token)
    assert payload["sub"] == uid
    assert payload["email"] == "test@fuga.plus"


def test_decode_token_invalido():
    with pytest.raises(UnauthenticatedException):
        decode_token("token_invalido_totalmente")
