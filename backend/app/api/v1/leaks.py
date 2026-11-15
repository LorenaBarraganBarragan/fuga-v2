"""
leaks.py — Endpoints de detección y consulta de posibles fugas (HU-23, HU-24)
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_current_user
from app.schemas.leaks import LeaksListResponse
from app.services.leaks_service import LeaksService

router = APIRouter(prefix="/leaks", tags=["leaks"])


@router.get("", response_model=LeaksListResponse)
def get_leaks(
    user: CurrentUser = Depends(get_current_user),
    db: Optional[Session] = Depends(lambda: None),
):
    """
    Detecta posibles patrones repetidos de gasto bajo demanda (FUGA-01 v1.0).
    Nunca muestra información de terceros (RF-033, D-15).
    """
    return LeaksService.detect_leaks(usuario_id=user.user_id, db=db)
