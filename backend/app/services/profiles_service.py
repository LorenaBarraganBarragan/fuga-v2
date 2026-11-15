"""
profiles_service.py — Servicio de dominio para gestión de perfiles de usuario
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.security import CurrentUser
from app.repositories.profiles import ProfilesRepository
from app.schemas.auth import ProfileResponse


class ProfilesService:
    @staticmethod
    def get_or_bootstrap_profile(
        user: CurrentUser,
        db: Optional[Session] = None,
        nombres: Optional[str] = None,
        apellido: Optional[str] = None,
    ) -> ProfileResponse:
        """
        Retorna el perfil del usuario o lo crea si no existe.
        Si la base de datos no está disponible, provee un perfil coherente basado en los claims.
        """
        if db is not None and isinstance(db, Session):
            repo = ProfilesRepository(user.user_id)
            profile = repo.ensure_profile(db, nombres=nombres, apellido=apellido)
            if profile:
                return profile

        # Fallback cuando no hay BD activa
        return ProfileResponse(
            id=user.user_id,
            nombres=nombres,
            apellido=apellido,
            rol=user.rol,
            disabled_at=user.disabled_at,
        )
