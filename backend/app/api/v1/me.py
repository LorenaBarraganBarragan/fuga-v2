"""Perfil propio y carga de imágenes controlada por backend."""

from typing import Literal
from urllib.parse import urlparse

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.errors import ForbiddenException, ValidationException
from app.core.security import CurrentUser, get_current_user, get_token_claims, require_user
from app.db.session import get_db
from app.repositories.profiles import ProfilesRepository
from app.schemas.auth import ProfileBootstrapRequest, ProfileResponse, ProfileUpdateRequest

router = APIRouter(prefix="/me", tags=["identity"])


class DeactivateRequest(BaseModel):
    confirmado: Literal[True]


@router.post("/deactivate")
def deactivate(
    body: DeactivateRequest,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    from app.services.accounts_service import change_state

    return change_state(user.user_id, False, user.user_id, db, allow_self=True)


class GooglePhoto(BaseModel):
    url: str = Field(max_length=2000)


@router.post("/photo/google", response_model=ProfileResponse)
def google_photo(
    body: GooglePhoto,
    claims: dict = Depends(get_token_claims),
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    if "google" not in claims.get("app_metadata", {}).get("providers", []):
        raise ForbiddenException("La cuenta no tiene una identidad Google vinculada.")
    try:
        parsed = urlparse(body.url)
        port = parsed.port
    except ValueError:
        raise ValidationException("Fotografía de Google no válida.") from None
    if (
        parsed.scheme != "https"
        or not (parsed.hostname or "").endswith(".googleusercontent.com")
        or parsed.username
        or parsed.password
        or port not in (None, 443)
    ):
        raise ValidationException("Fotografía de Google no válida.")
    db.execute(
        text("UPDATE perfil SET foto_google_url=:url WHERE id=:uid"),
        {"url": body.url, "uid": str(user.user_id)},
    )
    db.commit()
    return ProfilesRepository(user.user_id).get_profile(db)


@router.get("", response_model=ProfileResponse)
def get_current_user_profile(
    user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    return ProfilesRepository(user.user_id).get_profile(db)


@router.post("/bootstrap", response_model=ProfileResponse)
def bootstrap_profile(
    body: ProfileBootstrapRequest | None = None,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProfilesRepository(user.user_id).ensure_profile(
        db, body.nombres if body else None, body.apellido if body else None
    )


@router.patch("", response_model=ProfileResponse)
def update_profile(
    body: ProfileUpdateRequest,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    fields = body.model_dump(exclude_unset=True)
    # foto_url is set only by a verified upload, never an arbitrary client URL.
    if "foto_url" in fields:
        raise ValidationException("Utiliza el flujo de carga de fotografía.")
    if fields:
        clauses = ",".join(k + "=:" + k for k in fields)
        db.execute(
            text("UPDATE perfil SET " + clauses + " WHERE id=:uid"),
            {**fields, "uid": str(user.user_id)},
        )
        db.commit()
    return ProfilesRepository(user.user_id).get_profile(db)


class PhotoComplete(BaseModel):
    public_id: str = Field(max_length=180)


@router.post("/photo/signature")
def photo_signature(
    user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)
):
    from app.services.profile_photos import issue_upload

    return issue_upload(db, user.user_id)


@router.post("/photo/complete", response_model=ProfileResponse)
def photo_complete(
    body: PhotoComplete, user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)
):
    from app.services.profile_photos import complete_upload

    complete_upload(db, user.user_id, body.public_id)
    return ProfilesRepository(user.user_id).get_profile(db)


@router.post("/photo/cancel")
def photo_cancel(
    body: PhotoComplete, user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)
):
    from app.services.profile_photos import cancel_upload

    return cancel_upload(db, user.user_id, body.public_id)
