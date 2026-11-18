from uuid import uuid4

import pytest

from app.api.v1.me import GooglePhoto, google_photo, photo_signature
from app.core.config import settings
from app.core.errors import ForbiddenException, UpstreamException, ValidationException
from app.core.security import CurrentUser


def test_photo_upload_unavailable_is_explicit(monkeypatch):
    monkeypatch.setattr(settings, "CLOUDINARY_API_SECRET", None)
    with pytest.raises(UpstreamException):
        photo_signature(CurrentUser(uuid4()))


def test_google_photo_requires_google_identity():
    with pytest.raises(ForbiddenException):
        google_photo(
            GooglePhoto(url="https://lh3.googleusercontent.com/a"),
            {},
            CurrentUser(uuid4()),
            object(),
        )


@pytest.mark.parametrize(
    "url",
    [
        "http://lh3.googleusercontent.com/a",
        "https://googleusercontent.com.evil.invalid/a",
        "https://evil.invalid/a",
    ],
)
def test_google_photo_rejects_untrusted_urls(url):
    with pytest.raises(ValidationException):
        google_photo(
            GooglePhoto(url=url),
            {"app_metadata": {"providers": ["google"]}},
            CurrentUser(uuid4()),
            object(),
        )


def test_deactivation_requires_explicit_confirmation():
    from pydantic import ValidationError

    from app.api.v1.me import DeactivateRequest

    with pytest.raises(ValidationError):
        DeactivateRequest(confirmado=False)
