"""
session.py — Conexión a base de datos PostgreSQL con SQLAlchemy 2.0
"""

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings
from app.core.errors import UpstreamException

Base = declarative_base()

_engine = None
_SessionFactory = None


def get_engine():
    global _engine, _SessionFactory
    if _engine is None and settings.database_url:
        # pool_pre_ping=True verifica la conexión antes de entregarla
        _engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            hide_parameters=True,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=10,
            pool_recycle=1800,
            connect_args={
                "connect_timeout": settings.DB_CONNECT_TIMEOUT,
                "options": (
                    f"-c statement_timeout={settings.DB_STATEMENT_TIMEOUT_MS} "
                    f"-c lock_timeout={settings.DB_LOCK_TIMEOUT_MS}"
                ),
            },
        )
        _SessionFactory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine,
        )
    return _engine


def get_db() -> Generator[Session, None, None]:
    """Dependencia para inyección de sesión de base de datos."""
    try:
        engine = get_engine()
    except SQLAlchemyError:
        raise UpstreamException("La configuración de PostgreSQL no está disponible.") from None
    if engine is None or _SessionFactory is None:
        raise UpstreamException("Base de datos no configurada o no disponible.")

    db = _SessionFactory()
    try:
        yield db
    except SQLAlchemyError:
        db.rollback()
        raise UpstreamException("No se pudo completar la operación en la base de datos.") from None
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def check_db_health() -> bool:
    """Verifica si la base de datos responde a una consulta simple."""
    try:
        engine = get_engine()
        if engine is None:
            return False
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
