"""Provider failures are explicit and cannot undo the local account block."""

from types import SimpleNamespace
from uuid import uuid4

import httpx
import pytest

from app.api.v1.admin import AccountState, state
from app.api.v1.me import DeactivateRequest, deactivate
from app.core.config import settings
from app.core.errors import ForbiddenException, UpstreamException
from app.core.security import CurrentUser


class Database:
    def __init__(self):
        self.sql = []
        self.commits = 0

    def execute(self, statement, params=None):
        self.sql.append(str(statement))
        return SimpleNamespace(first=lambda: ("usuario",))

    def commit(self):
        self.commits += 1


@pytest.mark.parametrize("status_code", [None, 401, 403])
def test_failed_provider_reports_pending_but_commits_block(monkeypatch, status_code):
    db = Database()
    monkeypatch.setattr(settings, "SUPABASE_SERVICE_ROLE_KEY", "local-test-only")

    def fail(*a, **kw):
        if status_code is not None:
            response = httpx.Response(
                status_code,
                request=httpx.Request("PUT", "https://supabase.example.test/auth/v1/admin/users"),
            )
            response.raise_for_status()
        raise httpx.ConnectError("offline")

    monkeypatch.setattr("app.services.accounts_service.httpx.put", fail)
    with pytest.raises(UpstreamException):
        state(uuid4(), AccountState(activo=False), CurrentUser(uuid4(), rol="administrador"), db)
    assert db.commits == 1
    assert any("auth_sync_pendiente=TRUE" in sql for sql in db.sql)
    assert not any("auth_sync_pendiente=FALSE" in sql for sql in db.sql)


def test_admin_cannot_disable_self(monkeypatch):
    db = Database()
    uid = uuid4()
    monkeypatch.setattr(settings, "SUPABASE_SERVICE_ROLE_KEY", "local-test-only")
    with pytest.raises(ForbiddenException):
        state(uid, AccountState(activo=False), CurrentUser(uid, rol="administrador"), db)
    assert db.commits == 0


def test_provider_missing_no_fake_success(monkeypatch):
    monkeypatch.setattr(settings, "SUPABASE_SERVICE_ROLE_KEY", None)
    db = Database()
    with pytest.raises(UpstreamException):
        state(uuid4(), AccountState(activo=True), CurrentUser(uuid4(), rol="administrador"), db)
    assert db.sql == []


@pytest.mark.parametrize("operation", ["activate", "disable", "deactivate_self"])
def test_provider_success_uses_apikey_without_bearer(monkeypatch, operation):
    db = Database()
    uid = uuid4()
    active = operation == "activate"
    secret = "sb_secret_local-test-only"
    monkeypatch.setattr(settings, "SUPABASE_SERVICE_ROLE_KEY", secret)
    monkeypatch.setattr(settings, "SUPABASE_URL", "https://supabase.example.test")
    requests = []

    def respond(request):
        assert db.commits == 0
        assert request.method == "PUT"
        assert str(request.url) == f"https://supabase.example.test/auth/v1/admin/users/{uid}"
        assert request.headers["apikey"] == secret
        assert "authorization" not in request.headers
        assert request.read() == (
            b'{"ban_duration":"none"}' if active else b'{"ban_duration":"876000h"}'
        )
        requests.append(request)
        return httpx.Response(200, json={"id": str(uid)})

    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        monkeypatch.setattr("app.services.accounts_service.httpx.put", client.put)
        if operation == "deactivate_self":
            result = deactivate(DeactivateRequest(confirmado=True), CurrentUser(uid), db)
        else:
            result = state(
                uid, AccountState(activo=active), CurrentUser(uuid4(), rol="administrador"), db
            )
    assert len(requests) == 1
    assert result["auth_sincronizado"]
    assert result["activo"] is active
    assert db.commits == 1
