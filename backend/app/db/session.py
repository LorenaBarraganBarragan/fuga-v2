"""
session.py — Conexión a base de datos PostgreSQL con SQLAlchemy 2.0
"""

from typing import Generator, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings
from app.core.errors import UpstreamException

Base = declarative_base()

_engine = None
_SessionFactory = None


def get_engine():
    global _engine, _SessionFactory
    if _engine is None and settings.DATABASE_URL:
        # pool_pre_ping=True verifica la conexión antes de entregarla
        _engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        _SessionFactory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine,
        )
    return _engine


def get_db() -> Generator[Session, None, None]:
    """Dependencia para inyección de sesión de base de datos."""
    engine = get_engine()
    if engine is None or _SessionFactory is None:
        raise UpstreamException("Base de datos no configurada o no disponible.")

    db = _SessionFactory()
    try:
        yield db
    finally:
        db.close()


def check_db_health() -> bool:
    """Verifica si la base de datos responde a una consulta simple."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
