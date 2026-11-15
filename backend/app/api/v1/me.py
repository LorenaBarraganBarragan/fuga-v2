"""
me.py — Endpoints de identidad del usuario actual (GET /me y POST /me/bootstrap)
"""

from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_current_user, get_db
from app.schemas.auth import ProfileBootstrapRequest, ProfileResponse
from app.services.profiles_service import ProfilesService

router = APIRouter(prefix="/me", tags=["identity"])


@router.get("", response_model=ProfileResponse)
def get_current_user_profile(
    user: CurrentUser = Depends(get_current_user),
    db: Optional[Session] = Depends(lambda: None),
):
    """Retorna el perfil del usuario autenticado."""
    return ProfilesService.get_or_bootstrap_profile(user=user, db=db)


@router.post("/bootstrap", response_model=ProfileResponse)
def bootstrap_profile(
    body: ProfileBootstrapRequest = None,
    user: CurrentUser = Depends(get_current_user),
    db: Optional[Session] = Depends(lambda: None),
):
    """
    Garantiza de forma idempotente que el perfil del usuario exista en la base de datos.
    Compatible con el trigger de auth.users (C-02).
    """
    nombres = body.nombres if body else None
    apellido = body.apellido if body else None
    return ProfilesService.get_or_bootstrap_profile(
        user=user,
        db=db,
        nombres=nombres,
        apellido=apellido,
    )
