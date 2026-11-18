"""USB-only QA: real JWT verification, disposable LOCAL financial database.

The operator must use the existing fictitious Auth account. The first verified
subject is pinned for this process; this does not change production provisioning.
Never loads backend dotenv or any service-role key. No Auth admin operations.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from threading import Lock
from urllib.parse import urlsplit
from uuid import UUID, uuid4

import psycopg
import uvicorn
from dotenv import dotenv_values
from psycopg import sql
from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[2]
ADMIN_DSN = "postgresql://fuga_test@127.0.0.1:55440/postgres"
PORT = 18000


def validate_local_dsn(dsn):
    info = psycopg.conninfo.conninfo_to_dict(dsn)
    if info.get("host") != "127.0.0.1" or info.get("hostaddr"):
        raise ValueError("QA requiere PostgreSQL loopback explícito.")
    if info.get("port") != "55440" or info.get("user") != "fuga_test":
        raise ValueError("QA requiere el clúster desechable separado.")
    return info


@contextmanager
def disposable_database():
    info = validate_local_dsn(ADMIN_DSN)
    name = "fuga_android_qa_" + uuid4().hex
    with psycopg.connect(**info, autocommit=True) as admin:
        admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
        try:
            with psycopg.connect(**{**info, "dbname": name}, autocommit=True) as db:
                db.execute("""DO $$ BEGIN
                  IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='anon') THEN
                    CREATE ROLE anon; END IF;
                  IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='authenticated') THEN
                    CREATE ROLE authenticated; END IF;
                  IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='supabase_auth_admin') THEN
                    CREATE ROLE supabase_auth_admin; END IF;
                END $$;
                CREATE SCHEMA auth;
                CREATE TABLE auth.users(
                  id uuid PRIMARY KEY,email text,raw_user_meta_data jsonb DEFAULT '{}',
                  created_at timestamptz DEFAULT now());
                GRANT USAGE ON SCHEMA auth TO supabase_auth_admin,authenticated;
                GRANT INSERT,SELECT ON auth.users TO supabase_auth_admin;
                CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql AS $$
                  SELECT (nullif(current_setting('request.jwt.claims',true),'')::jsonb
                          ->>'sub')::uuid
                $$;""")
                for migration in sorted((ROOT / "supabase/migrations").glob("*.sql")):
                    db.execute(migration.read_text(encoding="utf-8-sig"))
            yield name
        finally:
            if not re.fullmatch(r"fuga_android_qa_[0-9a-f]{32}", name):
                raise RuntimeError("Nombre QA no válido; no se elimina ninguna base.")
            admin.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))


class QaIdentityGate:
    def __init__(self):
        self._subject = None
        self._lock = Lock()

    @property
    def bound(self):
        return self._subject is not None

    def provision_verified_claims(self, claims, engine):
        from app.core.errors import ForbiddenException

        subject = UUID(claims["sub"])
        with self._lock:
            if self._subject is not None and self._subject != subject:
                raise ForbiddenException(
                    "Este entorno QA admite una sola cuenta ficticia por sesión."
                )
            if self._subject is None:
                # Only the verified test subject is mirrored. No email/metadata from Auth.
                with engine.begin() as connection:
                    connection.execute(
                        text("""INSERT INTO auth.users(id,email)
                        VALUES (:id,'qa@local.invalid') ON CONFLICT DO NOTHING"""),
                        {"id": subject},
                    )
                self._subject = subject

    def statistics(self, engine):
        subject = self._subject
        if subject is None:
            return {"expense_count": 0, "total_cop": 0, "current_leaks": 0}
        with engine.connect() as connection:
            row = connection.execute(
                text("""SELECT count(*),coalesce(sum(monto_cop),0) FROM gasto
                     WHERE usuario_id=:uid AND deleted_at IS NULL"""),
                {"uid": subject},
            ).one()
            leaks = connection.execute(
                text("SELECT count(*) FROM fuga WHERE usuario_id=:uid AND vigente"),
                {"uid": subject},
            ).scalar_one()
        return {"expense_count": row[0], "total_cop": int(row[1]), "current_leaks": leaks}


def install_qa_controls(app, engine, gate, *, photos=False):
    from fastapi import Header
    from fastapi.responses import JSONResponse

    from app.core.security import get_token_claims

    def qa_claims(authorization: str | None = Header(None)):
        # Same signature, issuer, audience, expiry and UUID validation as production.
        claims = get_token_claims(authorization)
        gate.provision_verified_claims(claims, engine)
        return claims

    app.dependency_overrides[get_token_claims] = qa_claims
    counters = Counter()
    counter_lock = Lock()

    @app.middleware("http")
    async def qa_boundary(request, call_next):
        path = request.url.path
        permitted_photo = photos and path in {
            "/api/v1/me/photo/signature", "/api/v1/me/photo/complete", "/api/v1/me/photo/cancel"
        }
        if (path.startswith(("/api/v1/admin", "/api/v1/me/deactivate"))
                or (path.startswith("/api/v1/me/photo") and not permitted_photo)):
            return JSONResponse(
                {"error": {"code": "QA_LOCAL_ONLY", "message": "Operación fuera del ensayo QA."}},
                status_code=403,
                headers={"X-Fuga-QA": "local-disposable"},
            )
        response = await call_next(request)
        response.headers["X-Fuga-QA"] = "local-disposable"
        group = next(
            (name for name in ("me", "categories", "expenses", "analytics", "leaks")
             if path.startswith("/api/v1/" + name)),
            "other",
        )
        with counter_lock:
            counters[f"{request.method} {group} {response.status_code}"] += 1
        return response

    @app.get("/_qa/status", include_in_schema=False)
    def qa_status():
        with counter_lock:
            observed = dict(counters)
        return {
            "scope": "local-disposable",
            "auth": "original Supabase JWKS validation",
            "jwks_preflight": bool(getattr(app.state, "qa_jwks_preflight", False)),
            "photo_routes_enabled": photos,
            "fictitious_account_bound": gate.bound,
            **gate.statistics(engine),
            "requests_without_personal_data": observed,
        }


def photo_credentials():
    """Backend only. No database/admin keys or other dotenv values enter QA settings."""
    names = ("CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET")
    values = dotenv_values(ROOT / "backend/.env.local", interpolate=False)
    result = {name: values.get(name) for name in names}
    if not all(isinstance(value, str) and value.strip() for value in result.values()):
        raise ValueError("Falta configuración Cloudinary de servidor; no se muestran valores.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--photos", action="store_true",
                        help="Requiere autorización de cargas Cloudinary; BD exclusivamente local.")
    args = parser.parse_args()
    port = 18001 if args.photos else PORT
    cloud = photo_credentials() if args.photos else {}
    # Only the public Auth URL is needed. No backend/.env or private key is read.
    public = dotenv_values(ROOT / "mobile/.env.local")
    url = public.get("EXPO_PUBLIC_SUPABASE_URL") or ""
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https" or not parsed.hostname or parsed.path not in {"", "/"}
        or parsed.username or parsed.password or parsed.query or parsed.fragment
    ):
        raise ValueError("Revisa la URL pública raíz de Supabase sin compartir su valor.")
    environment = {
        name: value for name, value in os.environ.items()
        if name.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP"}
    }
    os.environ.clear()
    os.environ.update(environment)
    os.environ.update(
        APP_ENV="test", FUGA_LOAD_DOTENV="0", LOG_LEVEL="WARNING", SUPABASE_URL=url,
        SUPABASE_JWT_AUDIENCE="authenticated", CORS_ORIGINS="[]",
    )
    os.environ.update(cloud)
    sys.path.insert(0, str(ROOT / "backend"))
    state = ROOT / (".tools/android-qa/state-photos.json" if args.photos
                    else ".tools/android-qa/state.json")
    state.parent.mkdir(parents=True, exist_ok=True)
    with disposable_database() as name:
        os.environ["DATABASE_URL"] = (
            "postgresql+psycopg://fuga_test@127.0.0.1:55440/" + name
        )
        from app.core.config import settings
        from app.core.security import jwks_client
        from app.db.session import get_engine
        from app.main import app

        engine = get_engine()
        gate = QaIdentityGate()
        if not jwks_client(settings.jwks_url).get_signing_keys():
            raise ValueError("JWKS público sin claves verificables.")
        app.state.qa_jwks_preflight = True
        install_qa_controls(app, engine, gate, photos=args.photos)
        state.write_text(json.dumps({"pid": os.getpid(), "port": port, "database": name,
                                     "scope": "local-disposable"}), encoding="utf-8")
        try:
            uvicorn.run(app, host="127.0.0.1", port=port, access_log=False, log_level="warning")
        finally:
            engine.dispose()
            state.write_text(json.dumps({"port": port, "running": False}), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(  # noqa: T201 - Fixed CLI diagnostic without configuration values.
            "No se pudo iniciar QA local; revisa el clúster desechable "
            "y la configuración pública.", file=sys.stderr
        )
        sys.exit(1)
