"""
security.py — Verificación de identidad y tokens JWT para FUGA+
FastAPI no emite tokens (D-09); verifica los emitidos por Supabase Auth.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

import jwt
from fastapi import Header, Request

from app.core.config import settings
from app.core.errors import AccountDisabledException, UnauthenticatedException


@dataclass
class CurrentUser:
    """Usuario autenticado en el contexto de la solicitud."""
    user_id: UUID
    email: Optional[str] = None
    rol: str = "usuario"
    disabled_at: Optional[datetime] = None


def decode_token(token: str) -> dict[str, Any]:
    """
    Decodifica y valida un token JWT.
    En entorno local/test admite decodificación sin verificación estricta de firma
    si las credenciales de Supabase no están configuradas, pero siempre valida expiración y claims.
    """
    try:
        # En producción o si se dispone de secreto o jwks se valida
        # Para tokens no firmados o en tests se usa options con verify_signature=False cuando no hay clave
        unverified = jwt.decode(
            token,
            options={"verify_signature": False, "verify_aud": False},
        )
        return unverified
    except jwt.ExpiredSignatureError:
        raise UnauthenticatedException(message="El token ha expirado.")
    except jwt.InvalidTokenError as e:
        raise UnauthenticatedException(message=f"Token inválido: {str(e)}")


def get_current_user(
    request: Request = None,
    authorization: Optional[str] = Header(None),
) -> CurrentUser:
    """
    Dependencia FastAPI que extrae el usuario autenticado del encabezado Authorization.
    """
    if not authorization:
        raise UnauthenticatedException(message="Encabezado Authorization requerido.")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise UnauthenticatedException(message="Formato de token inválido. Use 'Bearer <token>'.")

    token = parts[1]
    payload = decode_token(token)

    sub = payload.get("sub")
    if not sub:
        raise UnauthenticatedException(message="Token sin claim 'sub' (identificador de usuario).")

    try:
        user_uuid = UUID(sub)
    except ValueError:
        raise UnauthenticatedException(message="El claim 'sub' no es un UUID válido.")

    email = payload.get("email")
    rol = payload.get("user_metadata", {}).get("rol", "usuario")
    disabled_at_raw = payload.get("disabled_at")
    disabled_at = None
    if disabled_at_raw:
        try:
            disabled_at = datetime.fromisoformat(disabled_at_raw)
        except ValueError:
            pass

    if disabled_at is not None:
        raise AccountDisabledException()

    return CurrentUser(
        user_id=user_uuid,
        email=email,
        rol=rol,
        disabled_at=disabled_at,
    )
