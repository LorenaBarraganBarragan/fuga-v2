"""
categories.py — Endpoint de consulta del catálogo de categorías (D-02)
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_db
from app.core.security import require_user
from app.repositories.categories import CategoriesRepository

router = APIRouter(prefix="/categories", tags=["categories"])


class CategoryResponse(BaseModel):
    id: UUID
    nombre: str
    orden: int
    activa: bool


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Devuelve las 9 categorías del catálogo ordenadas por su orden oficial."""
    repo = CategoriesRepository()
    return repo.list_all(db)
