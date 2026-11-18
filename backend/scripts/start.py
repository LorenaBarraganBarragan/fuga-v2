"""Portable single-process launcher for the prepared Render service."""

import os
import sys
from pathlib import Path

import uvicorn
from pydantic import ValidationError


def main():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    os.environ.setdefault("APP_ENV", "prod")
    try:
        port = int(os.environ.get("PORT", "8000"))
        if not 1 <= port <= 65535:
            raise ValueError()
        from app.core.config import settings
    except (ValueError, ValidationError):
        # Do not print pydantic input dictionaries, connection strings or exceptions.
        print(  # noqa: T201 - CLI diagnostic with no configuration values.
            "Configuración de arranque inválida. "
            "Revisa las variables y el certificado, sin compartir sus valores.",
            file=sys.stderr,
        )
        return 2
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # noqa: S104 - Required platform listener; API authorization stays enabled.
        port=port,
        workers=1,
        log_level=settings.LOG_LEVEL.lower(),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
