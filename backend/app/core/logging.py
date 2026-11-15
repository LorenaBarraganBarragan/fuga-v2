"""
logging.py — Configuración de logging seguro para FUGA+ (RNF-007)
Filtra estrictamente claves sensibles: password, token, authorization, monto_cop, secret, etc.
"""

from __future__ import annotations

import logging
import re
from typing import Any

CLAVES_SENSIBLES = {
    "password",
    "contrasena",
    "contraseña",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "monto_cop",
    "monto",
    "secret",
    "service_role",
    "api_key",
    "jwt",
}


def sanitizar_datos(dato: Any) -> Any:
    """
    Sanitiza recursivamente diccionarios o listas eliminando o enmascarando
    claves sensibles antes de escribir a los logs.
    """
    if isinstance(dato, dict):
        sanitizado = {}
        for k, v in dato.items():
            if str(k).lower() in CLAVES_SENSIBLES:
                sanitizado[k] = "[REDACTED]"
            else:
                sanitizado[k] = sanitizar_datos(v)
        return sanitizado
    elif isinstance(dato, (list, tuple)):
        return [sanitizar_datos(item) for item in dato]
    elif isinstance(dato, str):
        # Enmascarar tokens JWT (formato header.payload.signature)
        if re.search(r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", dato):
            dato = re.sub(
                r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
                "[REDACTED_JWT]",
                dato,
            )
        return dato
    return dato


class SensitiveFilter(logging.Filter):
    """Filtro de logging para eliminar valores sensibles de los mensajes."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = sanitizar_datos(record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = sanitizar_datos(record.args)
            elif isinstance(record.args, (list, tuple)):
                record.args = tuple(sanitizar_datos(a) for a in record.args)
        return True


def setup_logging(level: str = "INFO") -> None:
    """Configura el logger raíz con el filtro de datos sensibles."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(numeric_level)

    # Remover handlers existentes si los hay
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] [cid:%(correlation_id)s] %(message)s",
        defaults={"correlation_id": "-"},
    )
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SensitiveFilter())
    logger.addHandler(console_handler)


logger = logging.getLogger("fuga_plus")
