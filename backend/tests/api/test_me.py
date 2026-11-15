"""
test_me.py — Pruebas de endpoints /me y bootstrap (HU-01, HU-02, HU-04, F3)
"""

import uuid
from app.api.v1.me import get_current_user_profile, bootstrap_profile
from app.core.security import CurrentUser
from app.schemas.auth import ProfileBootstrapRequest


def test_get_current_user_profile():
    uid = uuid.uuid4()
    user = CurrentUser(user_id=uid, email="test@fuga.plus", rol="usuario")
    profile = get_current_user_profile(user=user)

    assert profile.id == uid
    assert profile.rol == "usuario"
    assert profile.disabled_at is None


def test_bootstrap_profile_idempotente():
    uid = uuid.uuid4()
    user = CurrentUser(user_id=uid, email="test@fuga.plus", rol="usuario")
    req = ProfileBootstrapRequest(nombres="Carlos", apellido="Gómez")

    p1 = bootstrap_profile(body=req, user=user)
    p2 = bootstrap_profile(body=req, user=user)

    assert p1.id == p2.id == uid
    assert p1.nombres == p2.nombres == "Carlos"
