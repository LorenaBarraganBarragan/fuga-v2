import pytest


@pytest.mark.parametrize(
    "path",
    [
        "/me",
        "/categories",
        "/expenses",
        "/analytics/summary",
        "/analytics/by-category",
        "/analytics/comparison",
        "/leaks",
        "/leaks/monthly-summary?periodo=2026-01",
        "/admin/users",
        "/admin/stats",
    ],
)
def test_private_get_routes_reject_anonymous(client, path):
    assert client.get("/api/v1" + path).status_code == 401


def test_forged_profile_role_is_rejected(private_client):
    from pydantic import ValidationError

    from app.schemas.auth import ProfileUpdateRequest

    with pytest.raises(ValidationError):
        ProfileUpdateRequest(rol="administrador")


def test_jwks_unavailable_never_falls_back_to_unverified(signer, monkeypatch):
    import jwt

    from app.core.errors import UpstreamException
    from app.core.security import decode_token

    token = signer()

    def unavailable(*args):
        raise jwt.PyJWKClientConnectionError("offline")

    monkeypatch.setattr("app.core.security.jwks_client", unavailable)
    with pytest.raises(UpstreamException):
        decode_token(token)
