"""Persistencia transaccional de gastos propios."""

import base64
import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.errors import (
    IdempotencyConflictException,
    IdempotencyExpiredException,
    NotFoundException,
    ValidationException,
)
from app.repositories.base import ScopedRepository
from app.schemas.expenses import ExpenseCreate, ExpenseResponse

SELECT_GASTO = (
    "SELECT g.*, c.nombre AS categoria_nombre FROM gasto g JOIN categoria c ON c.id=g.categoria_id"
)


def lock_user(db, uid):
    db.execute(text("SELECT pg_advisory_xact_lock(hashtextextended(:uid, 0))"), {"uid": str(uid)})


def as_expense(row):
    return ExpenseResponse.model_validate(dict(row))


class ExpensesRepository(ScopedRepository):
    def create(self, db: Session, expense: ExpenseCreate, clave_idempotencia: UUID):
        lock_user(db, self.usuario_id)
        params = {"uid": str(self.usuario_id), "key": str(clave_idempotencia)}
        row = (
            db.execute(
                text(SELECT_GASTO + " WHERE g.usuario_id=:uid AND g.clave_idempotencia=:key"),
                params,
            )
            .mappings()
            .first()
        )
        canonical = expense.model_dump(mode="json", exclude={"texto_original"})
        fingerprint = hashlib.sha256(json.dumps(canonical, sort_keys=True).encode()).hexdigest()
        now = datetime.now(timezone.utc)
        if row:
            created = row["created_at"]
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            if now - created > timedelta(hours=24):
                raise IdempotencyExpiredException()
            legacy_equal = all(
                str(row[k]) == str(canonical[k])
                for k in ("monto_cop", "descripcion", "fecha_gasto", "categoria_id")
            )
            if (row.get("request_hash") and row["request_hash"] != fingerprint) or (
                not row.get("request_hash") and not legacy_equal
            ):
                raise IdempotencyConflictException()
            # Preserve the original response even if the expense was edited or soft-deleted.
            return ExpenseResponse.model_validate(row.get("idempotency_response") or dict(row)), 200
        params.update(canonical)
        params.update({"id": str(uuid4()), "hash": fingerprint, "now": now})
        db.execute(
            text("""INSERT INTO gasto
          (id, usuario_id, categoria_id, monto_cop, descripcion, texto_original, fecha_gasto,
           moneda, diccionario_version, reglas_version, clave_idempotencia, request_hash, created_at, updated_at)
          VALUES (:id,:uid,:categoria_id,:monto_cop,:descripcion,NULL,:fecha_gasto,
           'COP',:diccionario_version,:reglas_version,:key,:hash,:now,:now)"""),
            params,
        )
        self.invalidate_leaks(db)
        result = self.get_by_id(db, UUID(params["id"]))
        db.execute(
            text(
                "UPDATE gasto SET idempotency_response=CAST(:body AS jsonb) WHERE id=:id AND usuario_id=:uid"
            ),
            {"body": result.model_dump_json(), "id": params["id"], "uid": params["uid"]},
        )
        db.commit()
        return result, 201

    def get_by_id(self, db, expense_id):
        row = (
            db.execute(
                text(
                    SELECT_GASTO + " WHERE g.id=:id AND g.usuario_id=:uid AND g.deleted_at IS NULL"
                ),
                {"id": str(expense_id), "uid": str(self.usuario_id)},
            )
            .mappings()
            .first()
        )
        if row is None:
            raise NotFoundException("Gasto no encontrado.")
        return as_expense(row)

    def list_paginated(self, db, limit=20, cursor=None, desde=None, hasta=None, categoria_id=None):
        if desde and hasta and desde > hasta:
            raise ValidationException("La fecha inicial no puede superar la final.")
        query = SELECT_GASTO + " WHERE g.usuario_id=:uid AND g.deleted_at IS NULL"
        params = {"uid": str(self.usuario_id), "limit": min(max(limit, 1), 50) + 1}
        for key, value, clause in (
            ("desde", desde, "g.fecha_gasto >= :desde"),
            ("hasta", hasta, "g.fecha_gasto <= :hasta"),
            ("cat", str(categoria_id) if categoria_id else None, "g.categoria_id = :cat"),
        ):
            if value is not None:
                query += " AND " + clause
                params[key] = value
        if cursor:
            try:
                values = json.loads(base64.b64decode(cursor, validate=True))
                if not isinstance(values, list) or len(values) != 3:
                    raise ValueError()
                params.update(
                    cf=date.fromisoformat(values[0]),
                    ct=datetime.fromisoformat(values[1]),
                    ci=str(UUID(values[2])),
                )
                query += " AND (g.fecha_gasto, g.created_at, g.id) < (:cf,:ct,:ci)"
            except (ValueError, TypeError, KeyError):
                raise ValidationException("Cursor inválido.") from None
        query += " ORDER BY g.fecha_gasto DESC, g.created_at DESC, g.id DESC LIMIT :limit"
        rows = db.execute(text(query), params).mappings().all()
        more = len(rows) == params["limit"]
        items = [as_expense(r) for r in rows[: params["limit"] - 1]]
        next_cursor = None
        if more and items:
            last = items[-1]
            next_cursor = base64.b64encode(
                json.dumps(
                    [str(last.fecha_gasto), last.created_at.isoformat(), str(last.id)]
                ).encode()
            ).decode()
        return items, next_cursor, more

    def invalidate_leaks(self, db):
        db.execute(
            text(
                "UPDATE fuga SET vigente=FALSE, actualizada_en=now() WHERE usuario_id=:uid AND vigente=TRUE"
            ),
            {"uid": str(self.usuario_id)},
        )

    def update(self, db, expense_id, body):
        lock_user(db, self.usuario_id)
        self.get_by_id(db, expense_id)
        params = body.model_dump(exclude={"texto_original"})
        params.update(
            id=str(expense_id), uid=str(self.usuario_id), categoria_id=str(body.categoria_id)
        )
        db.execute(
            text("""UPDATE gasto SET monto_cop=:monto_cop, descripcion=:descripcion,
          fecha_gasto=:fecha_gasto, categoria_id=:categoria_id, updated_at=now()
          WHERE id=:id AND usuario_id=:uid AND deleted_at IS NULL"""),
            params,
        )
        self.invalidate_leaks(db)
        self.audit_change(db, expense_id, "gasto_actualizado")
        result = self.get_by_id(db, expense_id)
        db.commit()
        return result

    def delete(self, db, expense_id):
        lock_user(db, self.usuario_id)
        self.get_by_id(db, expense_id)
        db.execute(
            text(
                "UPDATE gasto SET deleted_at=now(),updated_at=now() WHERE id=:id AND usuario_id=:uid"
            ),
            {"id": str(expense_id), "uid": str(self.usuario_id)},
        )
        self.invalidate_leaks(db)
        self.audit_change(db, expense_id, "gasto_eliminado")
        db.commit()

    def audit_change(self, db, expense_id, action):
        db.execute(
            text(
                "INSERT INTO auditoria (actor_id,accion,objetivo_id,resultado) VALUES (:uid,:accion,:id,'ok')"
            ),
            {"uid": str(self.usuario_id), "accion": action, "id": str(expense_id)},
        )
