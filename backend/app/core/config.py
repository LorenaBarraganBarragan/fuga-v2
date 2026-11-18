"""
config.py — Configuración central de FUGA+ mediante pydantic-settings
"""

import os
import ssl
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    APP_ENV: str = "local"
    LOG_LEVEL: str = "INFO"
    PROJECT_NAME: str = "FUGA+ API"
    API_V1_PREFIX: str = "/api/v1"

    # Supabase / Auth
    SUPABASE_URL: str = "https://placeholder.supabase.co"
    SUPABASE_JWKS_URL: str | None = None
    SUPABASE_JWT_ISSUER: str | None = None
    SUPABASE_JWT_AUDIENCE: str = "authenticated"
    SUPABASE_SERVICE_ROLE_KEY: str | None = Field(None, repr=False)

    # Base de datos
    DATABASE_URL: str | None = Field(None, repr=False)
    DATABASE_SSL_ROOT_CERT: Path | None = None
    DB_POOL_SIZE: int = Field(3, ge=1, le=10)
    DB_MAX_OVERFLOW: int = Field(2, ge=0, le=10)
    DB_CONNECT_TIMEOUT: int = Field(5, ge=1, le=30)
    DB_STATEMENT_TIMEOUT_MS: int = Field(15000, ge=1000, le=120000)
    DB_LOCK_TIMEOUT_MS: int = Field(5000, ge=1000, le=30000)
    CLOUDINARY_CLOUD_NAME: str | None = None
    CLOUDINARY_API_KEY: str | None = None
    CLOUDINARY_API_SECRET: str | None = Field(None, repr=False)

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:8081", "http://localhost:19006"]

    model_config = SettingsConfigDict(
        env_file=None
        if os.environ.get("APP_ENV", "local").lower() in {"prod", "production", "test"}
        or os.environ.get("FUGA_LOAD_DOTENV") == "0"
        else (
            Path(__file__).resolve().parents[2] / ".env",
            Path(__file__).resolve().parents[2] / ".env.local",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    @property
    def database_url(self) -> str | None:
        if not self.DATABASE_URL:
            return None
        try:
            url = make_url(self.DATABASE_URL)
            certificate = self.DATABASE_SSL_ROOT_CERT or url.query.get("sslrootcert")
            if certificate:
                path = Path(str(certificate))
                if not path.is_absolute():
                    path = BACKEND_ROOT / path
                url = url.update_query_dict({"sslrootcert": str(path.resolve())})
            return url.render_as_string(hide_password=False)
        except Exception:
            raise ValueError(
                "La configuración PostgreSQL no es válida; revisa controlador y SSL."
            ) from None

    @model_validator(mode="after")
    def validate_production(self):
        self.SUPABASE_URL = self.SUPABASE_URL.rstrip("/")
        self.APP_ENV = self.APP_ENV.lower()
        if self.APP_ENV == "production":
            self.APP_ENV = "prod"
        if self.APP_ENV not in {"local", "test", "prod"}:
            raise ValueError("APP_ENV debe ser local, test o prod.")
        if self.APP_ENV != "prod":
            return self
        try:
            root = urlsplit(self.SUPABASE_URL)
            _ = root.port  # Raises for invalid ports without disclosing their values.
            if (
                root.scheme != "https"
                or not root.hostname
                or "placeholder" in root.hostname
                or root.path not in {"", "/"}
                or root.query
                or root.fragment
                or root.username
                or root.password
            ):
                raise ValueError()
            if self.SUPABASE_JWT_AUDIENCE != "authenticated":
                raise ValueError()
            if (
                self.SUPABASE_JWT_ISSUER
                and self.SUPABASE_JWT_ISSUER.rstrip("/") != self.SUPABASE_URL + "/auth/v1"
            ):
                raise ValueError()
            if (
                self.SUPABASE_JWKS_URL
                and self.SUPABASE_JWKS_URL != self.SUPABASE_URL + "/auth/v1/.well-known/jwks.json"
            ):
                raise ValueError()
            for origin in self.CORS_ORIGINS:
                parsed = urlsplit(origin)
                if (
                    parsed.scheme != "https"
                    or not parsed.hostname
                    or parsed.path not in {"", "/"}
                    or parsed.query
                    or parsed.fragment
                    or parsed.username
                    or parsed.password
                ):
                    raise ValueError()
            if not self.DATABASE_URL:
                raise ValueError()
            url = make_url(self.database_url)
            if (
                url.drivername != "postgresql+psycopg"
                or not url.host
                or not url.username
                or not url.database
            ):
                raise ValueError()
            if url.query.get("sslmode") != "verify-full" or not url.query.get("sslrootcert"):
                raise ValueError()
            ssl.create_default_context(cafile=str(url.query["sslrootcert"]))
            if self.LOG_LEVEL.upper() not in {"INFO", "WARNING", "ERROR", "CRITICAL"}:
                raise ValueError()
        except Exception:
            raise ValueError(
                "Configuración prod incompleta: revisa URL raíz Auth, CORS HTTPS, "
                "PostgreSQL/Psycopg, verify-full, certificado y nivel de logs. "
                "No se muestran valores."
            ) from None
        return self

    @property
    def jwks_url(self) -> str:
        if self.SUPABASE_JWKS_URL:
            return self.SUPABASE_JWKS_URL
        return f"{self.SUPABASE_URL.rstrip('/')}/auth/v1/.well-known/jwks.json"

    @property
    def jwt_issuer(self) -> str:
        if self.SUPABASE_JWT_ISSUER:
            return self.SUPABASE_JWT_ISSUER
        return f"{self.SUPABASE_URL.rstrip('/')}/auth/v1"


settings = Settings()
