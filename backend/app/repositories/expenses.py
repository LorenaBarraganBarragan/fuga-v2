"""
expenses.py — Repositorio de gastos con control estricto de idempotencia y paginación por cursor (F6)
"""

from __future__ import annotations

import base64
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.errors import (
    IdempotencyConflictException,
    IdempotencyExpiredException,
    NotFoundException,
    ValidationException,
)
from app.repositories.base import ScopedRepository
from app.schemas.expenses import ExpenseCreate, ExpenseResponse

ZONA_BOGOTA = ZoneInfo("America/Bogota")


class ExpensesRepository(ScopedRepository):
    """Acceso y persistencia de gastos con scoping estricto e idempotencia (RF-013, RF-033)."""

    def __init__(self, usuario_id: UUID):
        super().__init__(usuario_id)

    def create(
        self,
        db: Session,
        expense: ExpenseCreate,
        clave_idempotencia: UUID,
    ) -> Tuple[ExpenseResponse, int]:
        """
        Crea un gasto o devuelve el existente si la clave coincide.
        Retorna (ExpenseResponse, http_status_code):
          - 201 si es nueva creación
          - 200 si es repetición idéntica (RN-IDM-02)
        Lanza:
          - 409 IdempotencyConflictException si el contenido difiere
          - 409 IdempotencyExpiredException si la clave superó las 24 horas
        """
        # 1. Buscar si la clave de idempotencia ya fue utilizada por este usuario
        result = db.execute(
            text(
                "SELECT id, usuario_id, categoria_id, monto_cop, descripcion, texto_original, "
                "fecha_gasto, moneda, diccionario_version, reglas_version, clave_idempotencia, "
                "created_at, updated_at, deleted_at "
                "FROM gasto "
                "WHERE usuario_id = :uid AND clave_idempotencia = :clave"
            ),
            {"uid": str(self.usuario_id), "clave": str(clave_idempotencia)},
        )
        row = result.fetchone()

        now_utc = datetime.now(timezone.utc)

        if row:
            created_at = row[11]
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)

            # Verificar ventana de 24 horas (C-03, RN-IDM-05)
            if now_utc - created_at > timedelta(hours=24):
                raise IdempotencyExpiredException()

            # Comparar contenido sustancial: monto, fecha, descripcion, categoria
            monto_existente = int(row[3])
            desc_existente = row[4]
            fecha_existente = row[6]
            cat_existente = str(row[2])

            if (
                monto_existente == expense.monto_cop
                and desc_existente == expense.descripcion
                and str(fecha_existente) == str(expense.fecha_gasto)
                and cat_existente == str(expense.categoria_id)
            ):
                # Repetición idéntica legítima -> 200 OK con mismo ID
                return (
                    ExpenseResponse(
                        id=UUID(str(row[0])),
                        usuario_id=UUID(str(row[1])),
                        categoria_id=UUID(str(row[2])),
                        monto_cop=row[3],
                        descripcion=row[4],
                        texto_original=row[5],
                        fecha_gasto=row[6],
                        moneda=row[7],
                        diccionario_version=row[8],
                        reglas_version=row[9],
                        clave_idempotencia=UUID(str(row[10])),
                        created_at=row[11],
                        updated_at=row[12],
                        deleted_at=row[13],
                    ),
                    200,
                )
            else:
                # Misma clave pero contenido distinto -> 409 Conflicto
                raise IdempotencyConflictException()

        # 2. Nueva creación -> 201 Created
        new_id = uuid4()
        now_ts = datetime.now(timezone.utc)

        db.execute(
            text(
                "INSERT INTO gasto ("
                "id, usuario_id, categoria_id, monto_cop, descripcion, texto_original, "
                "fecha_gasto, moneda, diccionario_version, reglas_version, clave_idempotencia, "
                "created_at, updated_at"
                ") VALUES ("
                ":id, :uid, :cat_id, :monto, :desc, :texto_orig, :fecha, :moneda, :dicc_v, :reglas_v, :clave, :now, :now"
                ")"
            ),
            {
                "id": str(new_id),
                "uid": str(self.usuario_id),
                "cat_id": str(expense.categoria_id),
                "monto": expense.monto_cop,
                "desc": expense.descripcion,
                "texto_orig": None,  # C-01: texto_original se persiste como NULL en MVP
                "fecha": expense.fecha_gasto,
                "moneda": "COP",
                "dicc_v": expense.diccionario_version,
                "reglas_v": expense.reglas_version,
                "clave": str(clave_idempotencia),
                "now": now_ts,
            },
        )
        db.commit()

        return (
            ExpenseResponse(
                id=new_id,
                usuario_id=self.usuario_id,
                categoria_id=expense.categoria_id,
                monto_cop=expense.monto_cop,
                descripcion=expense.descripcion,
                texto_original=None,
                fecha_gasto=expense.fecha_gasto,
                moneda="COP",
                diccionario_version=expense.diccionario_version,
                reglas_version=expense.reglas_version,
                clave_idempotencia=clave_idempotencia,
                created_at=now_ts,
                updated_at=now_ts,
                deleted_at=None,
            ),
            201,
        )

    def get_by_id(self, db: Session, expense_id: UUID) -> ExpenseResponse:
        """Obtiene un gasto por ID asegurando que pertenece al usuario propietario."""
        result = db.execute(
            text(
                "SELECT g.id, g.usuario_id, g.categoria_id, g.monto_cop, g.descripcion, g.texto_original, "
                "g.fecha_gasto, g.moneda, g.diccionario_version, g.reglas_version, g.clave_idempotencia, "
                "g.created_at, g.updated_at, g.deleted_at, c.nombre "
                "FROM gasto g "
                "JOIN categoria c ON c.id = g.categoria_id "
                "WHERE g.id = :id AND g.usuario_id = :uid AND g.deleted_at IS NULL"
            ),
            {"id": str(expense_id), "uid": str(self.usuario_id)},
        )
        row = result.fetchone()
        if not row:
            raise NotFoundException("Gasto no encontrado.")

        return ExpenseResponse(
            id=UUID(str(row[0])),
            usuario_id=UUID(str(row[1])),
            categoria_id=UUID(str(row[2])),
            categoria_nombre=row[14],
            monto_cop=row[3],
            descripcion=row[4],
            texto_original=row[5],
            fecha_gasto=row[6],
            moneda=row[7],
            diccionario_version=row[8],
            reglas_version=row[9],
            clave_idempotencia=UUID(str(row[10])),
            created_at=row[11],
            updated_at=row[12],
            deleted_at=row[13],
        )

    def list_paginated(
        self,
        db: Session,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> Tuple[List[ExpenseResponse], Optional[str], bool]:
        """
        Lista gastos paginados por cursor con orden canónico:
        fecha_gasto DESC, created_at DESC, id DESC (C-04, §16.8).
        """
        limit = min(max(1, limit), 50)
        query_sql = (
            "SELECT g.id, g.usuario_id, g.categoria_id, g.monto_cop, g.descripcion, g.texto_original, "
            "g.fecha_gasto, g.moneda, g.diccionario_version, g.reglas_version, g.clave_idempotencia, "
            "g.created_at, g.updated_at, g.deleted_at, c.nombre "
            "FROM gasto g "
            "JOIN categoria c ON c.id = g.categoria_id "
            "WHERE g.usuario_id = :uid AND g.deleted_at IS NULL "
        )
        params: Dict[str, Any] = {"uid": str(self.usuario_id), "lim": limit + 1}

        if cursor:
            # Desempaquetar cursor opaco
            try:
                decoded = base64.b64decode(cursor.encode()).decode()
                # Formato: fecha_gasto|created_at_iso|id
                parts = decoded.split("|")
                if len(parts) == 3:
                    c_fecha, c_created_at, c_id = parts
                    query_sql += (
                        "AND (g.fecha_gasto, g.created_at, g.id) < "
                        "(:c_fecha, :c_created_at, :c_id) "
                    )
                    params.update({
                        "c_fecha": c_fecha,
                        "c_created_at": c_created_at,
                        "c_id": c_id,
                    })
            except Exception:
                pass

        query_sql += "ORDER BY g.fecha_gasto DESC, g.created_at DESC, g.id DESC LIMIT :lim"

        result = db.execute(text(query_sql), params)
        rows = result.fetchall()

        has_more = len(rows) > limit
        items_rows = rows[:limit]

        items = [
            ExpenseResponse(
                id=UUID(str(r[0])),
                usuario_id=UUID(str(r[1])),
                categoria_id=UUID(str(r[2])),
                categoria_nombre=r[14],
                monto_cop=r[3],
                descripcion=r[4],
                texto_original=r[5],
                fecha_gasto=r[6],
                moneda=r[7],
                diccionario_version=r[8],
                reglas_version=r[9],
                clave_idempotencia=UUID(str(r[10])),
                created_at=r[11],
                updated_at=r[12],
                deleted_at=r[13],
            )
            for r in items_rows
        ]

        next_cursor = None
        if has_more and items:
            last = items[-1]
            raw_cursor = f"{last.fecha_gasto}|{last.created_at.isoformat()}|{last.id}"
            next_cursor = base64.b64encode(raw_cursor.encode()).decode()

        return items, next_cursor, has_more
