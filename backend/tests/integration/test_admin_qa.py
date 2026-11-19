"""Real local SQL + signed JWT verification. No financial QA database or remote HTTP."""
import json
import os
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import httpx
import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.core.config import settings
from app.core.security import (
    get_current_user,
    get_token_claims,
    jwks_client,
    require_admin,
    require_user,
)
from scripts.qa_admin_android import (
    PUBLIC_KEY,
    LocalAuth,
    administrative_database,
    create_qa_app,
    seed_accounts,
)

pytestmark = pytest.mark.integration


@pytest.fixture
def admin_qa(postgres_engine, monkeypatch):
    # postgres_engine ensures that the disposable cluster roles already exist.
    # This fixture NEVER reuses that DB or the running financial QA database.
    for k, v in {"FUGA_ADMIN_QA": "1", "APP_ENV": "test", "FUGA_LOAD_DOTENV": "0", "FUGA_RELEASE_BUILD": "0"}.items():
        monkeypatch.setenv(k, v)
    holder = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            self.dispatch()

        def do_POST(self):
            self.dispatch()

        def dispatch(self):
            if self.path == "/auth/v1/.well-known/jwks.json":
                code, body = 200, json.dumps(holder["auth"].jwks()).encode()
            else:
                length = int(self.headers.get("Content-Length", "0"))
                payload = self.rfile.read(length) if length else None
                response = holder["client"].request(self.command, self.path, headers=dict(self.headers), content=payload)
                code, body = response.status_code, response.content
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    with administrative_database() as name:
        engine = create_engine("postgresql+psycopg://fuga_test@127.0.0.1:55440/" + name, hide_parameters=True)
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        auth = LocalAuth(f"http://127.0.0.1:{server.server_port}")
        holder["auth"] = auth
        for k, v in {"APP_ENV": "test", "SUPABASE_URL": auth.origin, "SUPABASE_JWKS_URL": None,
                     "SUPABASE_JWT_ISSUER": None, "SUPABASE_SERVICE_ROLE_KEY": auth.service_key}.items():
            monkeypatch.setattr(settings, k, v)
        jwks_client.cache_clear()
        seed_accounts(engine, auth)
        app = create_qa_app(engine, auth, name)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with TestClient(app, base_url=auth.origin) as client:
                holder["client"] = client

                def provider(request):
                    # Only the provider HTTP call is simulated in tests; app role checks are real.
                    assert str(request.url).startswith(auth.issuer + "/admin/users/")
                    assert request.headers.get("apikey") == auth.service_key
                    assert "authorization" not in request.headers
                    response = client.put(request.url.path, headers={"apikey": auth.service_key}, content=request.content)
                    return httpx.Response(response.status_code, content=response.content)

                with httpx.Client(transport=httpx.MockTransport(provider)) as outgoing:
                    monkeypatch.setattr("app.services.accounts_service.httpx.put", outgoing.put)
                    yield client, auth, engine, app, name
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
            engine.dispose()
            jwks_client.cache_clear()


def login(client, auth, email="admin@admin-qa.invalid"):
    response = client.post("/auth/v1/token?grant_type=password", headers={"apikey": PUBLIC_KEY},
                           json={"email": email, "password": auth.password, "gotrue_meta_security": {}})
    assert response.status_code == 200
    return {"Authorization": "Bearer " + response.json()["access_token"]}


def test_local_admin_login_real_jwks_list_search_filter_detail_and_stats(admin_qa):
    client, auth, engine, app, _ = admin_qa
    assert not set(app.dependency_overrides) & {get_token_claims, get_current_user, require_admin, require_user}
    assert client.get("/api/v1/admin/users").status_code == 401
    headers = login(client, auth)
    assert client.get("/api/v1/me", headers=headers).json()["rol"] == "administrador"
    first = client.get("/api/v1/admin/users", headers=headers).json()
    assert first["total"] == 27 and len(first["items"]) == 20 and first["has_more"]
    second = client.get("/api/v1/admin/users?page=2", headers=headers).json()
    assert len(second["items"]) == 7 and not second["has_more"]
    assert not {x["id"] for x in first["items"]} & {x["id"] for x in second["items"]}
    assert client.get("/api/v1/admin/users?q=usuario01", headers=headers).json()["total"] == 1
    assert client.get("/api/v1/admin/users?q=Usuario%20ficticio%2001", headers=headers).json()["total"] == 1
    assert client.get("/api/v1/admin/users?q=no-match", headers=headers).json()["items"] == []
    active = client.get("/api/v1/admin/users?activo=true", headers=headers).json()
    inactive = client.get("/api/v1/admin/users?activo=false", headers=headers).json()
    assert active["total"] + inactive["total"] == 27
    assert all(x["disabled_at"] is None for x in active["items"])
    uid = inactive["items"][0]["id"]
    assert client.get("/api/v1/admin/users/" + uid, headers=headers).json()["id"] == uid
    stats = client.get("/api/v1/admin/stats", headers=headers).json()
    assert stats["registrados"] == 27 and len(stats["actividad_mensual"]) == 3
    with engine.connect() as db:
        assert db.execute(text("SELECT count(*) FROM auditoria")).scalar_one() >= 8


def test_roles_are_authoritative_and_admin_cannot_access_financial_routes(admin_qa):
    client, auth, _, _, _ = admin_qa
    admin = login(client, auth)
    normal = login(client, auth, "usuario01@admin-qa.invalid")
    assert client.get("/api/v1/admin/users", headers=normal).status_code == 403
    assert client.get("/api/v1/admin/stats", headers=normal).status_code == 403
    uid = next(a["id"] for a in auth.accounts.values() if a["admin"])
    assert client.patch(f"/api/v1/admin/users/{uid}/state", headers=normal, json={"activo": False}).status_code == 403
    assert client.patch("/api/v1/me", headers=normal, json={"rol": "administrador"}).status_code == 422
    claims = jwt.decode(normal["Authorization"].split()[1], options={"verify_signature": False})
    metadata_token = jwt.encode({**claims, "user_metadata": {"rol": "administrador"}}, auth.key,
                                algorithm="RS256", headers={"kid": auth.kid})
    assert client.get("/api/v1/admin/users", headers={"Authorization": "Bearer " + metadata_token}).status_code == 403
    for path in ["/expenses", "/analytics/summary", "/leaks"]:
        assert client.get("/api/v1" + path, headers=admin).status_code == 403


def test_local_activation_disabling_and_existing_sessions_use_original_service(admin_qa):
    client, auth, engine, _, _ = admin_qa
    admin = login(client, auth)
    normal = login(client, auth, "usuario01@admin-qa.invalid")
    uid = next(a["id"] for a in auth.accounts.values() if a["email"] == "usuario01@admin-qa.invalid")
    path = f"/api/v1/admin/users/{uid}/state"
    result = client.patch(path, headers=admin, json={"activo": False})
    assert result.status_code == 200 and result.json()["auth_sincronizado"]
    assert auth.accounts[uid]["disabled"]
    assert client.get("/api/v1/me", headers=normal).status_code == 403
    assert auth.login("usuario01@admin-qa.invalid", auth.password) is None
    with engine.connect() as db:
        assert db.execute(text("SELECT auth_sync_pendiente FROM perfil WHERE id=:id"), {"id": uid}).scalar_one() is False
        assert db.execute(text("SELECT estado FROM tarea_retencion WHERE usuario_id=:id"), {"id": uid}).scalar_one() == "pendiente"
    assert client.patch(path, headers=admin, json={"activo": True}).status_code == 200
    assert client.get("/api/v1/me", headers=login(client, auth, "usuario01@admin-qa.invalid")).status_code == 200
    with engine.connect() as db:
        assert db.execute(text("SELECT estado FROM tarea_retencion WHERE usuario_id=:id"), {"id": uid}).scalar_one() == "cancelada"
    aid = next(a["id"] for a in auth.accounts.values() if a["admin"])
    assert client.patch(f"/api/v1/admin/users/{aid}/state", headers=admin, json={"activo": False}).status_code == 403


@pytest.mark.parametrize("change", [{"exp": 1}, {"aud": "other"}, {"iss": "https://remote.invalid/auth/v1"}])
def test_original_jwt_validation_rejects_invalid_claims(admin_qa, change):
    client, auth, _, _, _ = admin_qa
    session = auth.login("admin@admin-qa.invalid", auth.password)
    claims = jwt.decode(session["access_token"], options={"verify_signature": False})
    token = jwt.encode({**claims, **change}, auth.key, algorithm="RS256", headers={"kid": auth.kid})
    assert client.get("/api/v1/admin/users", headers={"Authorization": "Bearer " + token}).status_code == 401
    invalid_signature = jwt.encode(claims, "fixture-signing-key-not-used-by-the-backend", algorithm="HS256", headers={"kid": auth.kid})
    assert client.get("/api/v1/admin/users", headers={"Authorization": "Bearer " + invalid_signature}).status_code == 401


def test_factory_and_provider_boundary_refuse_mixed_environment_and_other_accounts(admin_qa, monkeypatch):
    client, auth, engine, _, name = admin_qa
    assert client.get("/health", headers={"Host": "remote.invalid"}).status_code == 403
    assert client.get("/health", headers={"Origin": "https://other.invalid"}).status_code == 403
    assert client.post("/auth/v1/signup", json={}).status_code == 404
    assert client.put("/auth/v1/admin/users/00000000-0000-0000-0000-000000000001", headers={"apikey": PUBLIC_KEY}, json={"ban_duration": "none"}).status_code == 403
    assert client.put("/auth/v1/admin/users/00000000-0000-0000-0000-000000000001", headers={"apikey": auth.service_key}, json={"ban_duration": "none"}).status_code == 404
    with pytest.raises(ValueError):
        create_qa_app(engine, auth, "fuga_android_qa_" + "a" * 32)
    monkeypatch.setattr(settings, "SUPABASE_URL", "https://remote.invalid")
    with pytest.raises(ValueError):
        create_qa_app(engine, auth, name)
    monkeypatch.setenv("APP_ENV", "prod")
    with pytest.raises(ValueError):
        create_qa_app(engine, auth, name)


def test_real_mobile_sdk_login_refresh_user_and_logout_against_local_simulator(admin_qa):
    _, auth, _, _, _ = admin_qa
    root = Path(__file__).resolve().parents[3]
    program = r"""
const fs=require('node:fs'),assert=require('node:assert/strict');
const config=JSON.parse(fs.readFileSync(0,'utf8'));
const {createClient}=require('@supabase/supabase-js');
const {adminQaFetch,ADMIN_QA_ORIGIN,ADMIN_QA_PUBLIC_KEY}=require('./src/lib/adminQaAuth.ts');
const transport=adminQaFetch((url,options)=>{const u=new URL(url);return fetch(config.origin+u.pathname+u.search,options);});
const client=createClient(ADMIN_QA_ORIGIN,ADMIN_QA_PUBLIC_KEY,{global:{fetch:transport},auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false}});
(async()=>{
 const login=await client.auth.signInWithPassword({email:'admin@admin-qa.invalid',password:config.password});
 if(login.error)throw new Error('Local SDK login failed');
 const profile=await fetch(config.origin+'/api/v1/me',{headers:{Authorization:'Bearer '+login.data.session.access_token}});
 assert.equal((await profile.json()).rol,'administrador');
 assert.equal((await client.auth.refreshSession()).error,null);
 assert.equal((await client.auth.getUser()).data.user.email,'admin@admin-qa.invalid');
 assert.equal((await client.auth.signOut()).error,null);
 process.stdout.write('LOCAL_SDK_OK');
})().catch(()=>{process.stderr.write('LOCAL_SDK_FAILED');process.exitCode=1;});
"""
    environment = {k: v for k, v in os.environ.items() if k.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP"}}
    result = subprocess.run(["node", "-e", program], input=json.dumps({"origin": auth.origin, "password": auth.password}),
                            capture_output=True, text=True, timeout=25, cwd=root / "mobile", env=environment)
    assert result.returncode == 0, "Local SDK integration failed (no credentials logged)"
    assert result.stdout == "LOCAL_SDK_OK"
