"""Opt-in local administrative QA. Never imports real dotenv or contacts Supabase.

Only this CLI owns its disposable database. Production routers, JWT verification and
role dependencies remain unchanged. No HTTP server starts when this module is imported.
"""

import hashlib
import hmac
import json
import os
import re
import secrets
import socket
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import RLock
from unittest.mock import patch
from uuid import UUID, uuid4

import jwt
import psycopg
import uvicorn
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from psycopg import sql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[2]
ORIGIN = "http://127.0.0.1:18002"
PUBLIC_KEY = "sb_publishable_fugaplus_admin_qa"
DB_PREFIX = "fuga_admin_qa_"
CLUSTER = {"host": "127.0.0.1", "port": "55440", "user": "fuga_test", "dbname": "postgres"}


def require_qa_environment(environment):
    if (environment.get("FUGA_ADMIN_QA") != "1"
            or environment.get("APP_ENV") != "test"
            or environment.get("FUGA_LOAD_DOTENV") != "0"
            or environment.get("FUGA_RELEASE_BUILD", "0") != "0"):
        raise ValueError("El simulador requiere autorización QA explícita y no admite producción.")


@contextmanager
def exclusive_admin_run(directory=None):
    directory = directory or ROOT / ".tools/admin-qa"
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / "run.lock"
    # Refuse a second launcher before it can overwrite another run's local login file.
    with lock.open("x", encoding="utf-8") as owner:
        owner.write(str(os.getpid()))
        owner.flush()
        try:
            with socket.socket() as probe:
                probe.bind(("127.0.0.1", 18002))
            yield directory
        finally:
            # Close before unlink: Windows does not allow deleting an open file.
            owner.close()
            lock.unlink(missing_ok=True)


@contextmanager
def local_network_only():
    """Deny external destinations AND DNS, including accidental proxy configuration."""
    connect, resolve = socket.socket.connect, socket.getaddrinfo

    def local_connect(sock, address):
        if not isinstance(address, tuple) or address[0] != "127.0.0.1":
            raise OSError("Red externa deshabilitada en QA administrativo.")
        return connect(sock, address)

    def local_resolve(host, *args, **kwargs):
        if host != "127.0.0.1":
            raise OSError("DNS externo deshabilitado en QA administrativo.")
        return resolve(host, *args, **kwargs)

    with patch("socket.socket.connect", local_connect), patch("socket.getaddrinfo", local_resolve):
        yield


@contextmanager
def administrative_database():
    """No DSN parameter: a random database in the fixed disposable loopback cluster."""
    require_qa_environment(os.environ)
    name = DB_PREFIX + uuid4().hex
    with psycopg.connect(**CLUSTER, autocommit=True) as owner:
        owner.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
        try:
            with psycopg.connect(**{**CLUSTER, "dbname": name}, autocommit=True) as db:
                db.execute("""CREATE SCHEMA auth;
                  CREATE TABLE auth.users(id uuid PRIMARY KEY,email text,
                    raw_user_meta_data jsonb DEFAULT '{}',created_at timestamptz DEFAULT now());
                  GRANT USAGE ON SCHEMA auth TO supabase_auth_admin,authenticated;
                  GRANT INSERT,SELECT ON auth.users TO supabase_auth_admin;
                  CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql AS $$
                    SELECT (nullif(current_setting('request.jwt.claims',true),'')::jsonb->>'sub')::uuid
                  $$;""")
                for migration in sorted((ROOT / "supabase/migrations").glob("*.sql")):
                    db.execute(migration.read_text(encoding="utf-8-sig"))
            yield name
        finally:
            if not re.fullmatch(r"fuga_admin_qa_[0-9a-f]{32}", name):
                raise RuntimeError("Base no reconocida: no se elimina ninguna base.")
            owner.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))


class LocalAuth:
    def __init__(self, origin=ORIGIN):
        if (not re.fullmatch(r"http://127\.0\.0\.1:[0-9]{1,5}", origin)
                or not 1 <= int(origin.rsplit(":", 1)[1]) <= 65535):
            raise ValueError("Auth QA requiere loopback HTTP explícito.")
        self.origin = origin
        self.issuer = origin + "/auth/v1"
        self.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.kid = "admin-qa-" + uuid4().hex
        self.service_key = secrets.token_urlsafe(32)
        self.password = secrets.token_urlsafe(18)
        self.salt = secrets.token_bytes(16)
        self.password_hash = self._password_hash(self.password)
        self.lock = RLock()
        self.accounts = {}
        self.sessions = {}
        self.refresh_tokens = {}
        for i in range(27):
            uid = str(uuid4())
            self.accounts[uid] = {
                "id": uid, "email": "admin@admin-qa.invalid" if i == 0 else f"usuario{i:02d}@admin-qa.invalid",
                "admin": i == 0, "disabled": i > 0 and i % 3 == 0,
                "name": "Administrador QA" if i == 0 else f"Usuario ficticio {i:02d}",
            }

    def _password_hash(self, password):
        return hashlib.pbkdf2_hmac("sha256", password.encode(), self.salt, 100000)

    def jwks(self):
        return {"keys": [{**jwt.algorithms.RSAAlgorithm.to_jwk(self.key.public_key(), as_dict=True),
                          "kid": self.kid, "alg": "RS256", "use": "sig"}]}

    def user(self, account):
        return {"id": account["id"], "email": account["email"], "aud": "authenticated",
                "role": "authenticated", "app_metadata": {"provider": "email", "providers": ["email"]},
                "user_metadata": {}, "identities": [], "is_anonymous": False,
                "email_confirmed_at": "2026-01-01T00:00:00Z", "created_at": "2026-01-01T00:00:00Z"}

    def _session(self, account, session_id=None):
        now = int(time.time())
        session_id = session_id or str(uuid4())
        refresh = secrets.token_urlsafe(32)
        claims = {"sub": account["id"], "iss": self.issuer, "aud": "authenticated",
                  "iat": now, "exp": now + 900, "role": "authenticated",
                  "email": account["email"], "session_id": session_id}
        self.sessions[session_id] = account["id"]
        self.refresh_tokens[hashlib.sha256(refresh.encode()).digest()] = (session_id, now + 28800)
        return {"access_token": jwt.encode(claims, self.key, algorithm="RS256", headers={"kid": self.kid}),
                "token_type": "bearer", "expires_in": 900, "expires_at": now + 900,
                "refresh_token": refresh, "user": self.user(account)}

    def login(self, email, password):
        with self.lock:
            account = next((a for a in self.accounts.values() if a["email"] == email.strip().lower()), None)
            valid = hmac.compare_digest(self._password_hash(password), self.password_hash)
            if not account or not valid or account["disabled"]:
                return None
            return self._session(account)

    def refresh(self, token):
        with self.lock:
            entry = self.refresh_tokens.pop(hashlib.sha256(token.encode()).digest(), None)
            if not entry or entry[1] <= time.time():
                return None
            sid = entry[0]
            uid = self.sessions.get(sid)
            account = self.accounts.get(uid)
            if not account or account["disabled"]:
                return None
            return self._session(account, sid)

    def access(self, authorization):
        try:
            kind, token = authorization.split()
            if kind.lower() != "bearer":
                return None
            claims = jwt.decode(token, self.key.public_key(), algorithms=["RS256"], issuer=self.issuer,
                                audience="authenticated", options={"require": ["exp", "iat", "iss", "aud", "sub", "session_id"]})
            with self.lock:
                account = self.accounts.get(claims["sub"])
                if not account or account["disabled"] or self.sessions.get(claims["session_id"]) != account["id"]:
                    return None
            return claims
        except (jwt.PyJWTError, ValueError, TypeError, KeyError):
            return None

    def logout(self, claims, global_scope):
        with self.lock:
            for sid, uid in list(self.sessions.items()):
                if sid == claims["session_id"] or (global_scope and uid == claims["sub"]):
                    self.sessions.pop(sid)

    def change_state(self, uid, active):
        with self.lock:
            account = self.accounts.get(uid)
            if not account or account["admin"]:
                return False
            account["disabled"] = not active
            if not active:
                for sid, owner in list(self.sessions.items()):
                    if owner == uid:
                        self.sessions.pop(sid)
            return True


def seed_accounts(engine, auth):
    with engine.begin() as db:
        for account in auth.accounts.values():
            db.execute(text("INSERT INTO auth.users(id,email) VALUES (:id,:email)"), account)
            db.execute(text("""UPDATE perfil SET nombres=:name,apellido='QA',rol=:role,
              disabled_at=CASE WHEN :disabled THEN now() ELSE NULL END WHERE id=:id"""),
                       {**account, "role": "administrador" if account["admin"] else "usuario"})
        for months_back in range(3):
            month = datetime.now(timezone.utc).date().replace(day=1)
            for _ in range(months_back):
                month = (month - timedelta(days=1)).replace(day=1)
            for account in list(auth.accounts.values())[1:10 + months_back]:
                db.execute(text("INSERT INTO actividad_mensual(usuario_id,periodo) VALUES (:id,:month)"),
                           {"id": account["id"], "month": month})


def create_qa_app(engine, auth, database):
    require_qa_environment(os.environ)
    if not re.fullmatch(r"fuga_admin_qa_[0-9a-f]{32}", database):
        raise ValueError("QA administrativo requiere su propia base desechable.")
    if (engine.url.host != "127.0.0.1" or engine.url.port != 55440
            or engine.url.username != "fuga_test" or engine.url.database != database):
        raise ValueError("La conexión no pertenece al clúster QA permitido.")
    with engine.connect() as db:
        if db.execute(text("SELECT current_database()")).scalar_one() != database:
            raise ValueError("La base efectiva no coincide con la base QA.")
    from app.api.v1.router import api_v1_router
    from app.core.config import settings
    from app.db.session import get_db
    from app.main import app as production_app

    if (settings.APP_ENV != "test" or settings.SUPABASE_URL != auth.origin
            or settings.jwt_issuer != auth.issuer
            or settings.jwks_url != auth.issuer + "/.well-known/jwks.json"
            or settings.SUPABASE_SERVICE_ROLE_KEY != auth.service_key):
        raise ValueError("La configuración no corresponde al proveedor ficticio local.")
    api = FastAPI(title="FUGA+ Admin QA local", docs_url=None, redoc_url=None, openapi_url=None,
                  exception_handlers=production_app.exception_handlers)

    def database_session():
        with Session(engine) as db:
            try:
                yield db
            except Exception:
                db.rollback()
                raise

    # Only the DB dependency changes. JWT verification and every role check are ORIGINAL.
    api.dependency_overrides[get_db] = database_session
    api.include_router(api_v1_router, prefix="/api/v1")

    @api.middleware("http")
    async def boundary(request, call_next):
        if request.url.hostname != "127.0.0.1" or request.headers.get("origin"):
            return JSONResponse({"error": "QA requiere USB loopback y cliente nativo."}, status_code=403)
        path = request.url.path
        if path.startswith(("/api/v1/me/photo", "/api/v1/me/deactivate")):
            return JSONResponse({"error": "Operación fuera del ensayo administrativo."}, status_code=403)
        response = await call_next(request)
        response.headers["X-Fuga-QA"] = "admin-local-only"
        return response

    def failure():
        return JSONResponse({"code": "invalid_credentials", "msg": "Acceso QA no válido o cuenta inactiva."}, status_code=400)

    def client_key(request):
        return hmac.compare_digest(request.headers.get("apikey", ""), PUBLIC_KEY)

    @api.get("/auth/v1/.well-known/jwks.json")
    def jwks():
        return auth.jwks()

    @api.get("/auth/v1/settings")
    def auth_settings(request: Request):
        return {"external": {"email": True}, "disable_signup": True} if client_key(request) else failure()

    @api.post("/auth/v1/token")
    async def token(request: Request):
        if not client_key(request):
            return failure()
        try:
            data = await request.json()
            if (not isinstance(data, dict)
                    or any(not isinstance(v, str) or len(v) > 2048 for k, v in data.items() if k != "gotrue_meta_security")
                    or data.get("gotrue_meta_security", {}) != {}):
                return failure()
            grant = request.query_params.get("grant_type")
            if grant == "password" and set(data) <= {"email", "password", "gotrue_meta_security"}:
                result = auth.login(data.get("email", ""), data.get("password", ""))
            elif grant == "refresh_token" and set(data) == {"refresh_token"}:
                result = auth.refresh(data["refresh_token"])
            else:
                result = None
            return result or failure()
        except (ValueError, TypeError):
            return failure()

    @api.get("/auth/v1/user")
    def user(request: Request):
        claims = auth.access(request.headers.get("authorization", "")) if client_key(request) else None
        return auth.user(auth.accounts[claims["sub"]]) if claims else failure()

    @api.post("/auth/v1/logout")
    def logout(request: Request):
        claims = auth.access(request.headers.get("authorization", "")) if client_key(request) else None
        if not claims:
            return failure()
        auth.logout(claims, request.query_params.get("scope", "global") == "global")
        return JSONResponse({}, status_code=200)

    @api.put("/auth/v1/admin/users/{uid}")
    async def provider_state(uid: UUID, request: Request):
        if not hmac.compare_digest(request.headers.get("apikey", ""), auth.service_key):
            return JSONResponse({"msg": "Operación no autorizada."}, status_code=403)
        try:
            body = await request.json()
            if body not in ({"ban_duration": "none"}, {"ban_duration": "876000h"}):
                return failure()
            if not auth.change_state(str(uid), body["ban_duration"] == "none"):
                return JSONResponse({"msg": "Cuenta ficticia no disponible."}, status_code=404)
            return auth.user(auth.accounts[str(uid)])
        except (ValueError, TypeError):
            return failure()

    @api.get("/health")
    def health():
        return {"status": "ok", "scope": "admin-local-only"}

    @api.get("/ready")
    def ready():
        with engine.connect() as db:
            db.execute(text("SELECT 1"))
        return {"status": "ready", "scope": "admin-local-only"}

    return api


def main():
    # Refuse to turn a production process into a QA process by accident.
    if os.environ.get("APP_ENV", "local").lower() in {"prod", "production"} or os.environ.get("FUGA_RELEASE_BUILD") == "1":
        raise ValueError("QA administrativo no se ejecuta en producción.")
    if sys.argv[1:]:
        raise ValueError("El lanzador no admite DSN, host, puertos o cuentas externas.")
    environment = {k: v for k, v in os.environ.items() if k.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP"}}
    os.environ.clear()
    os.environ.update(environment, FUGA_ADMIN_QA="1", APP_ENV="test", FUGA_LOAD_DOTENV="0", LOG_LEVEL="WARNING",
                      SUPABASE_URL=ORIGIN, CORS_ORIGINS="[]", SUPABASE_JWT_AUDIENCE="authenticated")
    sys.path.insert(0, str(ROOT / "backend"))
    auth = LocalAuth()
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = auth.service_key
    with exclusive_admin_run() as directory, local_network_only(), administrative_database() as name:
        url = "postgresql+psycopg://fuga_test@127.0.0.1:55440/" + name
        os.environ["DATABASE_URL"] = url
        engine = create_engine(url, hide_parameters=True, pool_size=3, max_overflow=2,
                               connect_args={"connect_timeout": 5})
        state = directory / "state.json"
        credentials = directory / "login.local.json"
        try:
            seed_accounts(engine, auth)
            api = create_qa_app(engine, auth, name)
            credentials.write_text(json.dumps({"scope": "LOCAL FICTICIO, NO SUPABASE",
                "email": "admin@admin-qa.invalid", "password": auth.password}, indent=2), encoding="utf-8")
            state.write_text(json.dumps({"pid": os.getpid(), "port": 18002, "scope": "admin-local-only"}), encoding="utf-8")
            print("QA administrativo local: 18002. Acceso ficticio en .tools/admin-qa/login.local.json; no compartir.")  # noqa: T201
            uvicorn.run(api, host="127.0.0.1", port=18002, access_log=False, log_level="warning")
        finally:
            engine.dispose()
            credentials.unlink(missing_ok=True)
            state.write_text(json.dumps({"port": 18002, "running": False}), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("No se inició QA administrativo. Revisa PostgreSQL local y los puertos; no se muestran datos de acceso.", file=sys.stderr)  # noqa: T201
        sys.exit(1)
