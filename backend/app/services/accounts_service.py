"""Cambio de estado compartido: bloqueo persistido, sincronizaci?n y auditor?a."""

import httpx
from sqlalchemy import text

from app.core.config import settings
from app.core.errors import ForbiddenException, NotFoundException, UpstreamException


def audit(db, actor, action, target=None, result="ok"):
    db.execute(
        text("INSERT INTO auditoria(actor_id,accion,objetivo_id,resultado) VALUES (:a,:b,:c,:d)"),
        {"a": str(actor), "b": action, "c": str(target) if target else None, "d": result},
    )


def change_state(uid, active, actor_id, db, *, allow_self=False):
    if not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise UpstreamException("Administración de Auth no configurada.")
    row = db.execute(
        text("SELECT rol FROM perfil WHERE id=:id FOR UPDATE"), {"id": str(uid)}
    ).first()
    if not row:
        raise NotFoundException()
    if (uid == actor_id and not allow_self) or row[0] == "administrador":
        raise ForbiddenException("No se modifican cuentas administrativas desde esta operación.")
    if not active:
        # Keep the row lock across the provider call to serialize state changes.
        # Commit the local block even when the provider fails, then report the partial failure.
        db.execute(
            text(
                "UPDATE perfil SET disabled_at=coalesce(disabled_at,now()),auth_sync_pendiente=TRUE WHERE id=:id"
            ),
            {"id": str(uid)},
        )
        db.execute(
            text("""INSERT INTO tarea_retencion(usuario_id,suprimir_desde,estado)
          SELECT id,disabled_at+interval '30 days','pendiente' FROM perfil WHERE id=:id
          ON CONFLICT(usuario_id) DO UPDATE SET suprimir_desde=EXCLUDED.suprimir_desde,estado='pendiente'"""),
            {"id": str(uid)},
        )
        audit(db, actor_id, "desactivacion_local", uid)
    try:
        response = httpx.put(
            f"{settings.SUPABASE_URL}/auth/v1/admin/users/{uid}",
            headers={
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
            },
            json={"ban_duration": "none" if active else "876000h"},
            timeout=10,
        )
        response.raise_for_status()
    except httpx.HTTPError:
        audit(db, actor_id, "sincronizacion_auth", uid, "pendiente")
        db.commit()
        raise UpstreamException(
            "No se completó la sincronización con Supabase. Reintenta; la cuenta desactivada permanece bloqueada localmente."
        ) from None
    db.execute(
        text(
            "UPDATE perfil SET disabled_at="
            + ("NULL" if active else "coalesce(disabled_at,now())")
            + ",auth_sync_pendiente=FALSE WHERE id=:id"
        ),
        {"id": str(uid)},
    )
    if active:
        db.execute(
            text("UPDATE tarea_retencion SET estado='cancelada' WHERE usuario_id=:id"),
            {"id": str(uid)},
        )
    audit(db, actor_id, "cuenta_activada" if active else "cuenta_desactivada", uid)
    db.commit()
    return {"id": uid, "activo": active, "auth_sincronizado": True}
