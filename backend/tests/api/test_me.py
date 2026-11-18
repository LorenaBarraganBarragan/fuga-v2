from uuid import uuid4

from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.main import app
from app.schemas.auth import ProfileResponse


def test_profile_http(client, monkeypatch):
    uid = uuid4()
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid)
    app.dependency_overrides[get_db] = lambda: object()
    monkeypatch.setattr(
        "app.repositories.profiles.ProfilesRepository.get_profile",
        lambda self, db: ProfileResponse(id=uid),
    )
    assert client.get("/api/v1/me").json()["id"] == str(uid)


def test_profile_requires_auth(client):
    assert client.get("/api/v1/me").status_code == 401
