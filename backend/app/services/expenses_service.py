"""
expenses_service.py — Servicio de lógica de negocio para gastos personales (F6)
"""

from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.errors import ValidationException
from app.repositories.categories import CategoriesRepository
from app.repositories.expenses import ExpensesRepository
from app.schemas.expenses import ExpenseCreate, ExpenseResponse


class ExpensesService:
    @staticmethod
    def create_expense(
        usuario_id: UUID,
        expense: ExpenseCreate,
        clave_idempotencia: UUID,
        db: Session,
    ) -> Tuple[ExpenseResponse, int]:
        # 1. Validar que la categoría exista en el catálogo
        cats_repo = CategoriesRepository()
        cat = cats_repo.get_by_id(expense.categoria_id, db)
        if not cat:
            raise ValidationException(
                message=f"La categoría {expense.categoria_id} no existe en el catálogo.",
                details=[{"field": "categoria_id", "issue": "not_in_catalog"}],
            )

        # 2. Delegar creación transaccional al repositorio con control de idempotencia
        repo = ExpensesRepository(usuario_id=usuario_id)
        return repo.create(db, expense=expense, clave_idempotencia=clave_idempotencia)

    @staticmethod
    def get_expense(
        usuario_id: UUID,
        expense_id: UUID,
        db: Session,
    ) -> ExpenseResponse:
        repo = ExpensesRepository(usuario_id=usuario_id)
        return repo.get_by_id(db, expense_id=expense_id)

    @staticmethod
    def list_expenses(
        usuario_id: UUID,
        limit: int = 20,
        cursor: Optional[str] = None,
        db: Session = None,
    ) -> Tuple[List[ExpenseResponse], Optional[str], bool]:
        if db is None:
            from app.core.errors import UpstreamException

            raise UpstreamException("El historial requiere una conexión a PostgreSQL.")
        repo = ExpensesRepository(usuario_id=usuario_id)
        return repo.list_paginated(db, limit=limit, cursor=cursor)
