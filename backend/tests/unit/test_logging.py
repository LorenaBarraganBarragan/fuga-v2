"""
test_logging.py — Prueba de filtro de datos sensibles en logs (RNF-007, F2)
"""

import io
import logging

import pytest

from app.core.logging import SensitiveFilter, sanitizar_datos


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
    assert limpio["descripcion"] == "[REDACTED]"


def test_sanitizar_datos_jwt():
    raw_jwt = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgN_p_placeholder"
    )
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


@pytest.mark.parametrize("name", ["apikey", "ApiKey", "SUPABASE_SERVICE_ROLE_KEY"])
def test_supabase_header_and_setting_are_redacted_recursively(name):
    data = {"headers": [{name: "opaque-test-value"}], "status": 200}
    assert sanitizar_datos(data) == {
        "headers": [{name: "[REDACTED]"}],
        "status": 200,
    }


def test_secret_keys_are_redacted_in_free_text_and_nested_values():
    data = {
        "message": "first=sb_secret_fake-One_123; second=sb_secret_fake-Two_456",
        "items": ["Bearer sb_secret_fake-Three_789", ("sb_secret_fake-Four_012",)],
        "status": 200,
    }
    cleaned = sanitizar_datos(data)
    assert "sb_secret_" not in str(cleaned)
    assert str(cleaned).count("[REDACTED_SECRET]") == 4
    assert cleaned["status"] == 200


@pytest.mark.parametrize(
    ("message", "args"),
    [
        ("credential=sb_secret_fake-Log_123", ()),
        ("credential=%s", ("sb_secret_fake-Log_123",)),
        ("credential=%(credential)s", ({"credential": "sb_secret_fake-Log_123"},)),
        ({"headers": {"apikey": "opaque-test-value"}}, ()),
    ],
)
def test_log_output_masks_secret_keys_and_structured_headers(message, args):
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.addFilter(SensitiveFilter())
    record = logging.LogRecord("supabase-test", logging.INFO, "", 0, message, args, None)
    handler.handle(record)
    output = stream.getvalue()
    assert "sb_secret_" not in output
    assert "opaque-test-value" not in output
    assert "REDACTED" in output


def test_log_extra_fields_mask_named_and_embedded_secrets():
    record = logging.LogRecord("supabase-test", logging.INFO, "", 0, "status=ok", (), None)
    record.apikey = "opaque-test-value"
    record.SUPABASE_SERVICE_ROLE_KEY = "opaque-test-value"
    record.context = {"headers": {"ApiKey": "opaque-test-value"}}
    record.detail = "credential=sb_secret_fake-Extra_123"
    SensitiveFilter().filter(record)
    assert record.apikey == "[REDACTED]"
    assert record.SUPABASE_SERVICE_ROLE_KEY == "[REDACTED]"
    assert record.context == {"headers": {"ApiKey": "[REDACTED]"}}
    assert record.detail == "credential=[REDACTED_SECRET]"
    assert "sb_secret_" not in str(record.__dict__)
    assert record.getMessage() == "status=ok"
