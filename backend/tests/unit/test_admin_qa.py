import socket

import jwt
import pytest

from scripts.qa_admin_android import (
    LocalAuth,
    exclusive_admin_run,
    local_network_only,
    require_qa_environment,
)


@pytest.fixture
def local_auth():
    return LocalAuth()


@pytest.mark.parametrize("changes", [{"APP_ENV": "prod"}, {"APP_ENV": "local"},
    {"FUGA_ADMIN_QA": "0"}, {"FUGA_LOAD_DOTENV": "1"}, {"FUGA_RELEASE_BUILD": "1"}])
def test_simulator_requires_explicit_test_environment(changes):
    with pytest.raises(ValueError):
        require_qa_environment({"APP_ENV": "test", "FUGA_ADMIN_QA": "1", "FUGA_LOAD_DOTENV": "0", **changes})


@pytest.mark.parametrize("origin", ["https://real.invalid", "http://localhost:18002", "http://127.0.0.1:18002/path", "http://127.0.0.1:18002@other.invalid"])
def test_auth_refuses_remote_or_ambiguous_origin(origin):
    with pytest.raises(ValueError):
        LocalAuth(origin)


def test_local_session_has_valid_signature_and_rotating_refresh_logout(local_auth):
    auth = local_auth
    assert auth.login("admin@admin-qa.invalid", "wrong") is None
    result = auth.login("admin@admin-qa.invalid", auth.password)
    jwk = jwt.PyJWK.from_dict(auth.jwks()["keys"][0])
    claims = jwt.decode(result["access_token"], jwk.key, algorithms=["RS256"], issuer=auth.issuer, audience="authenticated")
    assert claims["role"] == "authenticated"  # Application role comes exclusively from PostgreSQL.
    assert auth.access("Bearer " + result["access_token"])
    refreshed = auth.refresh(result["refresh_token"])
    assert refreshed and auth.refresh(result["refresh_token"]) is None
    auth.logout(claims, True)
    assert auth.refresh(refreshed["refresh_token"]) is None
    assert auth.access("Bearer " + result["access_token"]) is None


def test_simulated_ban_only_changes_fixture_accounts_and_revokes_refresh(local_auth):
    auth = local_auth
    admin = next(a for a in auth.accounts.values() if a["admin"])
    user = next(a for a in auth.accounts.values() if not a["admin"] and not a["disabled"])
    session = auth.login(user["email"], auth.password)
    assert auth.change_state(user["id"], False)
    assert auth.login(user["email"], auth.password) is None
    assert auth.refresh(session["refresh_token"]) is None
    assert auth.change_state("unknown", False) is False
    assert auth.change_state(admin["id"], False) is False
    assert auth.change_state(user["id"], True)
    assert auth.login(user["email"], auth.password)


def test_simulator_blocks_external_connections_and_dns():
    with local_network_only():
        with pytest.raises(OSError), socket.socket() as sock:
            sock.connect(("192.0.2.1", 443))
        with pytest.raises(OSError):
            socket.getaddrinfo("provider.invalid", 443)


def test_second_launcher_cannot_overwrite_existing_qa_access(tmp_path):
    # Use only a temporary lock: do not start a server or write runtime credentials.
    (tmp_path / "run.lock").write_text("local-fixture-owner", encoding="utf-8")
    with pytest.raises(FileExistsError), exclusive_admin_run(tmp_path):
        pytest.fail("A second launcher must not enter")
    assert (tmp_path / "run.lock").read_text(encoding="utf-8") == "local-fixture-owner"
