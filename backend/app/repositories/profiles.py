"""
profiles.py — Repositorio para la tabla perfil (HU-01, HU-02, HU-04, HU-33)
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.errors import NotFoundException
from app.repositories.base import ScopedRepository
from app.schemas.auth import ProfileResponse


class ProfilesRepository(ScopedRepository):
    """Acceso y mutación de perfiles de usuario con scoping estricto."""

    def __init__(self, usuario_id: UUID):
        super().__init__(usuario_id)

    def get_profile(self, db: Session) -> Optional[ProfileResponse]:
        result = db.execute(
            text(
                "SELECT id, nombres, apellido, telefono, foto_url, rol, disabled_at, created_at, updated_at "
                "FROM perfil WHERE id = :uid"
            ),
            {"uid": str(self.usuario_id)},
        )
        row = result.fetchone()
        if not row:
            return None
        return ProfileResponse(
            id=UUID(str(row[0])),
            nombres=row[1],
            apellido=row[2],
            telefono=row[3],
            foto_url=row[4],
            rol=row[5],
            disabled_at=row[6],
            created_at=row[7],
            updated_at=row[8],
        )

    def ensure_profile(
        self,
        db: Session,
        nombres: Optional[str] = None,
        apellido: Optional[str] = None,
    ) -> ProfileResponse:
        """Crea el perfil si no existe (idempotente) o devuelve el existente."""
        existing = self.get_profile(db)
        if existing:
            return existing

        db.execute(
            text(
                "INSERT INTO perfil (id, nombres, apellido, rol) "
                "VALUES (:uid, :nombres, :apellido, 'usuario') "
                "ON CONFLICT (id) DO NOTHING"
            ),
            {"uid": str(self.usuario_id), "nombres": nombres, "apellido": apellido},
        )
        db.commit()
        return self.get_profile(db)
