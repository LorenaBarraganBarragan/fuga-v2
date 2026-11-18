from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.core.errors import AccountDisabledException, ForbiddenException, UnauthenticatedException
from app.core.security import CurrentUser, get_current_user, get_token_claims, require_user


@pytest.mark.parametrize("authorization", [None, "Basic a", "Bearer", "Bearer a b"])
def test_sin_token_valido(authorization):
    with pytest.raises(UnauthenticatedException):
        get_token_claims(authorization)


def test_estado_y_rol_persistidos(monkeypatch):
    uid = uuid4()
    profile = SimpleNamespace(id=uid, rol="usuario", disabled_at=None)
    monkeypatch.setattr(
        "app.repositories.profiles.ProfilesRepository.ensure_profile", lambda self, db: profile
    )
    db = SimpleNamespace(execute=lambda *a: None, commit=lambda: None)
    user = get_current_user({"sub": str(uid), "user_metadata": {"rol": "administrador"}}, db)
    assert user.rol == "usuario"
    profile.disabled_at = datetime.now(timezone.utc)
    with pytest.raises(AccountDisabledException):
        get_current_user({"sub": str(uid)}, db)


def test_admin_no_lee_finanzas():
    with pytest.raises(ForbiddenException):
        require_user(CurrentUser(uuid4(), rol="administrador"))
