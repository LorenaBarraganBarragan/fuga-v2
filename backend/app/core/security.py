"""Supabase identity: cryptographic verification and authoritative account state."""

from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo

import jwt
from fastapi import Depends, Header
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import (
    AccountDisabledException,
    ForbiddenException,
    UnauthenticatedException,
    UpstreamException,
)
from app.db.session import get_db


@dataclass
class CurrentUser:
    user_id: UUID
    email: str | None = None
    rol: str = "usuario"
    disabled_at: datetime | None = None


@lru_cache(maxsize=4)
def jwks_client(url: str) -> jwt.PyJWKClient:
    return jwt.PyJWKClient(url, cache_jwk_set=True, lifespan=300, timeout=5)


def decode_token(token: str) -> dict[str, Any]:
    try:
        header = jwt.get_unverified_header(token)
        if header.get("alg") not in {"RS256", "ES256"} or not header.get("kid"):
            raise UnauthenticatedException()
        key = jwks_client(settings.jwks_url).get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            key.key,
            algorithms=["RS256", "ES256"],
            issuer=settings.jwt_issuer,
            audience=settings.SUPABASE_JWT_AUDIENCE,
            options={"require": ["exp", "iat", "iss", "aud", "sub"]},
        )
        UUID(payload["sub"])
        return payload
    except jwt.PyJWKClientConnectionError:
        raise UpstreamException("No se pudo verificar la identidad con Supabase.") from None
    except (jwt.PyJWTError, ValueError, TypeError, KeyError):
        raise UnauthenticatedException() from None


def get_token_claims(authorization: str | None = Header(None)) -> dict[str, Any]:
    parts = (authorization or "").split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise UnauthenticatedException()
    return decode_token(parts[1])


def get_current_user(
    claims: dict = Depends(get_token_claims),
    db: Session = Depends(get_db),
) -> CurrentUser:
    from app.repositories.profiles import ProfilesRepository

    profile = ProfilesRepository(UUID(claims["sub"])).ensure_profile(db)
    if profile.disabled_at is not None:
        raise AccountDisabledException()
    db.execute(
        text(
            "INSERT INTO actividad_mensual(usuario_id,periodo) VALUES (:id,:periodo) ON CONFLICT DO NOTHING"
        ),
        {
            "id": str(profile.id),
            "periodo": datetime.now(ZoneInfo("America/Bogota")).date().replace(day=1),
        },
    )
    db.commit()
    return CurrentUser(profile.id, claims.get("email"), profile.rol, profile.disabled_at)


def require_user(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if user.rol != "usuario":
        raise ForbiddenException("Las cuentas administrativas no acceden a finanzas individuales.")
    return user


def require_admin(
    user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)
) -> CurrentUser:
    if user.rol != "administrador":
        db.execute(
            text(
                "INSERT INTO auditoria(actor_id,accion,resultado) VALUES (:id,'fallo_autorizacion','denegado')"
            ),
            {"id": str(user.user_id)},
        )
        db.commit()
        raise ForbiddenException()
    return user
