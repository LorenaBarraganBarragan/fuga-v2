"""
test_logging.py — Prueba de filtro de datos sensibles en logs (RNF-007, F2)
"""

import io
import logging
from app.core.logging import SensitiveFilter, sanitizar_datos, setup_logging


def test_sanitizar_datos_dict():
    dato = {
        "monto_cop": 50000,
        "password": "mi_clave_secreta",
        "token": "bearer 12345",
        "descripcion": "almuerzo",
    }
    limpio = sanitizar_datos(dato)
    assert limpio["monto_cop"] == "[REDACTED]"
    assert limpio["password"] == "[REDACTED]"
    assert limpio["token"] == "[REDACTED]"
    assert limpio["descripcion"] == "almuerzo"


def test_sanitizar_datos_jwt():
    raw_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgN_p_placeholder"
    limpio = sanitizar_datos(f"Bearer {raw_jwt}")
    assert "[REDACTED_JWT]" in limpio
    assert raw_jwt not in limpio


def test_log_stream_sensitive_filter():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.addFilter(SensitiveFilter())
    test_logger = logging.getLogger("test_sensitive_logger")
    test_logger.addHandler(handler)
    test_logger.setLevel(logging.INFO)

    test_logger.info("Usuario con datos: %s", {"password": "supersecreto", "monto_cop": 8000})

    output = stream.getvalue()
    assert "supersecreto" not in output
    assert "8000" not in output
    assert "[REDACTED]" in output
