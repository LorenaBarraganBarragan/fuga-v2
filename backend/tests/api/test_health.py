"""
test_health.py — Pruebas de endpoints /health y /ready (F2)
"""

import pytest

from app.api.v1.health import health_check, readiness_check
from app.core.errors import UpstreamException


def test_health_check():
    """El endpoint /health devuelve status ok y app FUGA+."""
    res = health_check()
    assert res["status"] == "ok"
    assert res["app"] == "FUGA+"


def test_readiness_check_sin_db():
    """Sin base de datos configurada, /ready lanza UpstreamException (503)."""
    with pytest.raises(UpstreamException) as exc_info:
        readiness_check()
    assert exc_info.value.code == "UPSTREAM_ERROR"
    assert exc_info.value.status_code == 503
