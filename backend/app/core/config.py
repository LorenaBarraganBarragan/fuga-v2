"""
config.py — Configuración central de FUGA+ mediante pydantic-settings
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "local"
    LOG_LEVEL: str = "INFO"
    PROJECT_NAME: str = "FUGA+ API"
    API_V1_PREFIX: str = "/api/v1"

    # Supabase / Auth
    SUPABASE_URL: str = "https://placeholder.supabase.co"
    SUPABASE_JWKS_URL: Optional[str] = None
    SUPABASE_JWT_ISSUER: Optional[str] = None
    SUPABASE_JWT_AUDIENCE: str = "authenticated"
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None

    # Base de datos
    DATABASE_URL: Optional[str] = None

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:8081", "http://localhost:19006"]

    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def jwks_url(self) -> str:
        if self.SUPABASE_JWKS_URL:
            return self.SUPABASE_JWKS_URL
        return f"{self.SUPABASE_URL}/auth/v1/.well-known/jwks.json"

    @property
    def jwt_issuer(self) -> str:
        if self.SUPABASE_JWT_ISSUER:
            return self.SUPABASE_JWT_ISSUER
        return f"{self.SUPABASE_URL}/auth/v1"


settings = Settings()
