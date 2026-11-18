"""Gastos privados y borradores que nunca se persisten."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Response
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_db
from app.core.errors import ValidationException
from app.core.security import require_user
from app.domain.expenses.interpreter import ValidacionError, interpretar
from app.repositories.categories import CategoriesRepository
from app.repositories.expenses import ExpensesRepository
from app.schemas.expenses import (
    ExpenseCreate,
    ExpenseListResponse,
    ExpenseResponse,
    InterpretRequest,
    InterpretResponse,
)
from app.services.expenses_service import ExpensesService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/interpret", response_model=InterpretResponse)
def interpret_expense(
    request: InterpretRequest,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    try:
        catalog = {c["nombre"]: c["id"] for c in CategoriesRepository().list_all(db)}
        return interpretar(request.texto, catalogo_ids=catalog).to_dict()
    except ValidacionError as exc:
        raise ValidationException(
            exc.mensaje, [{"field": exc.campo, "issue": "invalid_value"}]
        ) from None


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_expense(
    body: ExpenseCreate,
    response: Response,
    idempotency_key: UUID = Header(..., alias="Idempotency-Key"),
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    result, code = ExpensesService.create_expense(user.user_id, body, idempotency_key, db)
    response.status_code = code
    return result


@router.get("", response_model=ExpenseListResponse)
def list_expenses(
    limit: int = Query(20, ge=1, le=50),
    cursor: str | None = Query(None, max_length=512),
    desde: date | None = None,
    hasta: date | None = None,
    categoria_id: UUID | None = None,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    items, next_cursor, more = ExpensesRepository(user.user_id).list_paginated(
        db, limit, cursor, desde, hasta, categoria_id
    )
    return ExpenseListResponse(items=items, next_cursor=next_cursor, has_more=more)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: UUID, user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)
):
    return ExpensesRepository(user.user_id).get_by_id(db, expense_id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: UUID,
    body: ExpenseCreate,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    repo = ExpensesRepository(user.user_id)
    repo.get_by_id(db, expense_id)
    if not CategoriesRepository().get_by_id(body.categoria_id, db):
        raise ValidationException("Categoría no válida.")
    return repo.update(db, expense_id, body)


@router.delete("/{expense_id}", status_code=204)
def delete_expense(
    expense_id: UUID, user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)
):
    ExpensesRepository(user.user_id).delete(db, expense_id)
    return Response(status_code=204)
