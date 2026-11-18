from pathlib import Path

import pytest
from pydantic import ValidationError
from sqlalchemy.engine import make_url

from app.core.config import Settings

CERT = Path(__file__).resolve().parents[2] / "certs/prod-ca-2021.crt"


def configuration(**overrides):
    values = {
        "APP_ENV": "prod",
        "SUPABASE_URL": "https://project.example.test",
        "DATABASE_URL": (
            "postgresql+psycopg://test:private-test-password@db.example.test/postgres"
            "?sslmode=verify-full"
        ),
        "DATABASE_SSL_ROOT_CERT": CERT,
        "CORS_ORIGINS": [],
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_production_preserves_credentials_and_resolves_public_certificate():
    config = configuration()
    url = make_url(config.database_url)
    assert url.password == "private-test-password"
    assert url.host == "db.example.test"
    assert Path(url.query["sslrootcert"]) == CERT.resolve()
    assert url.query["sslmode"] == "verify-full"
    assert "private-test-password" not in repr(config)


@pytest.mark.parametrize(
    "overrides",
    [
        {"DATABASE_URL": None},
        {
            "DATABASE_URL": "postgresql://test:private-test-password@db.example.test/postgres?sslmode=verify-full"
        },
        {
            "DATABASE_URL": "postgresql+psycopg://test:private-test-password@db.example.test/postgres?sslmode=require"
        },
        {"DATABASE_SSL_ROOT_CERT": Path("missing-test-certificate.crt")},
        {"SUPABASE_URL": "https://project.example.test/auth/v1"},
        {"SUPABASE_URL": "http://project.example.test"},
        {"CORS_ORIGINS": ["*"]},
        {"CORS_ORIGINS": ["http://localhost:8081"]},
        {"LOG_LEVEL": "DEBUG"},
        {"SUPABASE_JWKS_URL": "https://other.example.test/jwks"},
        {"SUPABASE_JWT_ISSUER": "https://other.example.test/auth/v1"},
        {"SUPABASE_JWT_AUDIENCE": "unexpected-audience"},
        {"SUPABASE_URL": "https://project.example.test:not-a-port"},
    ],
)
def test_invalid_production_configuration_never_discloses_inputs(overrides):
    with pytest.raises(ValidationError) as error:
        configuration(**overrides)
    assert "private-test-password" not in str(error.value)


def test_local_without_external_services_remains_usable_for_tests():
    assert Settings(_env_file=None, APP_ENV="local", DATABASE_URL=None).database_url is None


def test_relative_certificate_is_resolved_from_backend_not_working_directory():
    assert (
        Path(
            make_url(
                configuration(DATABASE_SSL_ROOT_CERT=Path("certs/prod-ca-2021.crt")).database_url
            ).query["sslrootcert"]
        )
        == CERT.resolve()
    )


def test_password_reserved_characters_survive_url_normalization():
    from urllib.parse import quote

    password = "local:fixture@with/[reserved]#%?"
    config = configuration(
        DATABASE_URL="postgresql+psycopg://test:"
        + quote(password, safe="")
        + "@db.example.test/postgres?sslmode=verify-full"
    )
    assert make_url(config.database_url).password == password
    assert make_url(config.database_url).username == "test"


def test_server_pool_uses_bounded_connections_and_statement_timeouts(monkeypatch):
    from types import SimpleNamespace

    from app.db import session

    captured = {}

    def engine(url, **kwargs):
        captured.update(kwargs)
        return SimpleNamespace()

    monkeypatch.setattr(session, "settings", configuration())
    monkeypatch.setattr(session, "_engine", None)
    monkeypatch.setattr(session, "_SessionFactory", None)
    monkeypatch.setattr(session, "create_engine", engine)
    monkeypatch.setattr(session, "sessionmaker", lambda **kwargs: object())
    assert session.get_engine() is not None
    assert captured["pool_size"] + captured["max_overflow"] == 5
    assert captured["connect_args"]["connect_timeout"] == 5
    assert "statement_timeout=15000" in captured["connect_args"]["options"]
    assert "lock_timeout=5000" in captured["connect_args"]["options"]


def test_render_launcher_honors_port_and_runs_one_process(monkeypatch):
    import importlib.util

    from app.core import config

    path = Path(__file__).resolve().parents[2] / "scripts/start.py"
    spec = importlib.util.spec_from_file_location("prepared_render_start", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    calls = []
    monkeypatch.setenv("PORT", "10000")
    monkeypatch.setattr(config, "settings", configuration())
    monkeypatch.setattr(module.uvicorn, "run", lambda *a, **kw: calls.append(kw))
    assert module.main() == 0
    assert calls[0]["port"] == 10000
    assert calls[0]["workers"] == 1
    monkeypatch.setenv("PORT", "not-a-port")
    assert module.main() == 2
