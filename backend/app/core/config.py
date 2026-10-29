from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "http://localhost:19006,http://localhost:8081"
    
    MONGODB_URI: str = ""
    MONGODB_DB: str = "fuga_db"
    
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_ATTEMPT_WINDOW_MINUTES: int = 15
    LOCKOUT_MINUTES: int = 15
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    def validate_config(self):
        if self.APP_ENV != "development":
            if not self.JWT_SECRET_KEY or self.JWT_SECRET_KEY == "change-this-secret" or len(self.JWT_SECRET_KEY) < 32:
                raise ValueError("JWT_SECRET_KEY must be set to a secure value in non-development environments")
            if not self.MONGODB_URI:
                raise ValueError("MONGODB_URI must be configured")
        else:
            if self.JWT_SECRET_KEY and (self.JWT_SECRET_KEY == "change-this-secret" or len(self.JWT_SECRET_KEY) < 16):
                pass  # warn but allow in dev
            if not self.MONGODB_URI:
                pass  # warn but allow in dev
    
    def is_jwt_config_valid(self) -> bool:
        if not self.JWT_SECRET_KEY:
            return False
        if self.JWT_SECRET_KEY == "change-this-secret":
            return False
        if len(self.JWT_SECRET_KEY) < 32:
            return False
        return True

settings = Settings()
try:
    settings.validate_config()
except Exception as e:
    if settings.APP_ENV != "development":
        raise
    print(f"Config warning: {e}")
