"""Local test identities are cryptographically signed; never used by runtime."""

import time
from types import SimpleNamespace
from uuid import uuid4

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.security import CurrentUser, require_user
from app.db.session import get_db
from app.main import app


@pytest.fixture
def signer(monkeypatch):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    monkeypatch.setattr(
        "app.core.security.jwks_client",
        lambda url: SimpleNamespace(
            get_signing_key_from_jwt=lambda token: SimpleNamespace(key=key.public_key())
        ),
    )

    def sign(**overrides):
        now = int(time.time())
        claims = {
            "sub": str(uuid4()),
            "iss": settings.jwt_issuer,
            "aud": settings.SUPABASE_JWT_AUDIENCE,
            "exp": now + 600,
            "iat": now,
            **overrides,
        }
        return jwt.encode(claims, key, algorithm="RS256", headers={"kid": "local-test"})

    return sign


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def private_client(client):
    user = CurrentUser(uuid4())
    app.dependency_overrides[require_user] = lambda: user
    app.dependency_overrides[get_db] = lambda: object()
    return client
