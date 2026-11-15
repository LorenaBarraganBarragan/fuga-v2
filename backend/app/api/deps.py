"""
deps.py — Dependencias comunes inyectables en rutas de FastAPI
"""

from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db

__all__ = ["CurrentUser", "get_current_user", "get_db"]
