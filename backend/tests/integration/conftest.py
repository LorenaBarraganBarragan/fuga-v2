"""Disposable LOCAL PostgreSQL only. Never connects to Supabase."""

import os
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.main import app


@pytest.fixture(scope="session")
def postgres_engine():
    dsn = os.environ.get("FUGA_TEST_DATABASE_URL")
    if not dsn:
        pytest.skip("FUGA_TEST_DATABASE_URL no configurada; requiere PostgreSQL local desechable.")
    info = psycopg.conninfo.conninfo_to_dict(dsn)
    if info.get("host") not in {"127.0.0.1", "localhost", "::1"} or info.get("hostaddr"):
        pytest.fail("Las pruebas solo admiten PostgreSQL local; nunca Supabase remoto.")
    name = "fuga_test_" + uuid4().hex
    admin = psycopg.connect(dsn, autocommit=True)
    admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
    test_info = {**info, "dbname": name}
    conn = psycopg.connect(**test_info, autocommit=True)
    try:
        conn.execute("""DO $$ BEGIN
          IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='anon') THEN CREATE ROLE anon; END IF;
          IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='authenticated') THEN CREATE ROLE authenticated; END IF;
          IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='supabase_auth_admin') THEN CREATE ROLE supabase_auth_admin; END IF;
        END $$""")
        # Minimal provider substitute, only in the disposable local database.
        conn.execute("""CREATE SCHEMA auth;
          CREATE TABLE auth.users(id uuid PRIMARY KEY,email text,raw_user_meta_data jsonb DEFAULT '{}',created_at timestamptz DEFAULT now());
          GRANT USAGE ON SCHEMA auth TO supabase_auth_admin;
          GRANT INSERT,SELECT ON auth.users TO supabase_auth_admin;
          -- Reproduce permissive Supabase defaults to prove that migrations revoke them.
          ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO anon,authenticated;
        """)
        conn.execute("GRANT USAGE ON SCHEMA auth TO authenticated")
        conn.execute("""CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql AS $$
          SELECT (nullif(current_setting('request.jwt.claims',true),'')::jsonb->>'sub')::uuid $$""")
        conn.execute(
            "INSERT INTO auth.users(id,email) VALUES (%s,'preexisting@local.invalid')", (uuid4(),)
        )
        # SQL must target public explicitly even when the session has another search_path.
        conn.execute("SET search_path=pg_catalog")
        for path in sorted(
            (Path(__file__).resolve().parents[3] / "supabase" / "migrations").glob("*.sql")
        ):
            conn.execute(path.read_text(encoding="utf-8-sig"))
        # SQLAlchemy delegates DBAPI connections to this explicit local test configuration.
        engine = create_engine(
            "postgresql+psycopg://", creator=lambda: psycopg.connect(**test_info)
        )
        yield engine
        engine.dispose()
    finally:
        conn.close()
        if not name.startswith("fuga_test_"):
            raise RuntimeError("Refusing to remove a non-test database.")
        admin.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))
        admin.close()


@pytest.fixture
def database(postgres_engine):
    with Session(postgres_engine) as db:
        yield db
        db.rollback()


@pytest.fixture
def integrated_client(client, postgres_engine, signer):
    def dependency():
        with Session(postgres_engine) as db:
            try:
                yield db
            except Exception:
                db.rollback()
                raise

    app.dependency_overrides[get_db] = dependency
    return client
