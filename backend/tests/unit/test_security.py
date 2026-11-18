import jwt
import pytest

from app.core.errors import UnauthenticatedException
from app.core.security import decode_token


def test_decode_token_valido(signer):
    assert decode_token(signer())["sub"]


@pytest.mark.parametrize(
    "claims", [{"exp": 1}, {"aud": "otro"}, {"iss": "https://otro"}, {"sub": "no-uuid"}]
)
def test_claims_incorrectos(signer, claims):
    with pytest.raises(UnauthenticatedException):
        decode_token(signer(**claims))


def test_firma_alterada(signer):
    token = signer()
    pieces = token.split(".")
    pieces[2] = ("A" if pieces[2][0] != "A" else "B") + pieces[2][1:]
    with pytest.raises(UnauthenticatedException):
        decode_token(".".join(pieces))


@pytest.mark.parametrize(
    "token",
    [
        "invalido",
        jwt.encode({"sub": "x"}, "local-test-key-with-at-least-32-bytes", algorithm="HS256"),
        jwt.encode({"sub": "x"}, algorithm="none", key=""),
    ],
)
def test_tokens_no_confiables(token):
    with pytest.raises(UnauthenticatedException):
        decode_token(token)
