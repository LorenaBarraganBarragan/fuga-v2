"""
expenses.py — Rutas de gastos e interpretación de FUGA+
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Header, Query, status

from app.api.deps import CurrentUser, get_current_user, get_db
from app.core.errors import ValidationException
from app.domain.expenses.interpreter import ValidacionError, interpretar
from app.schemas.expenses import (
    ExpenseCreate,
    ExpenseListResponse,
    ExpenseResponse,
    InterpretRequest,
    InterpretResponse,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/interpret", response_model=InterpretResponse)
def interpret_expense(
    request: InterpretRequest,
    user: CurrentUser = Depends(get_current_user),
):
    """
    Interpreta texto libre de gasto y devuelve un borrador (Draft).
    NO persiste nada en base de datos (D-05, C-01).
    """
    try:
        draft = interpretar(request.texto)
        return draft.to_dict()
    except ValidacionError as e:
        raise ValidationException(
            message=e.mensaje,
            details=[{"field": e.campo, "issue": "invalid_value"}],
        )
