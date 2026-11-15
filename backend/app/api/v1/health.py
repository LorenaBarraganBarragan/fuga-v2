"""
health.py — Endpoints de salud y disponibilidad (/health y /ready)
"""

from fastapi import APIRouter
from app.core.errors import UpstreamException
from app.db.session import check_db_health

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """Liveness probe: el servicio está corriendo y responde."""
    return {"status": "ok", "app": "FUGA+"}


@router.get("/ready")
def readiness_check():
    """Readiness probe: verifica conectividad con la base de datos."""
    if not check_db_health():
        raise UpstreamException(message="La base de datos no está disponible.")
    return {"status": "ready", "database": "connected"}
