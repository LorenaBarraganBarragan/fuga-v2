"""
categories.py — Endpoint de consulta del catálogo de categorías (D-02)
"""

from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID

from app.api.deps import CurrentUser, get_current_user
from app.repositories.categories import CategoriesRepository

router = APIRouter(prefix="/categories", tags=["categories"])


class CategoryResponse(BaseModel):
    id: UUID
    nombre: str
    orden: int
    activa: bool


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    user: CurrentUser = Depends(get_current_user),
    db: Optional[Session] = Depends(lambda: None),
):
    """Devuelve las 9 categorías del catálogo ordenadas por su orden oficial."""
    repo = CategoriesRepository()
    return repo.list_all(db)
