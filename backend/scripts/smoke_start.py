"""Start the real production launcher using synthetic config and loopback only."""

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def main():
    root = Path(__file__).resolve().parents[1]
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    environment = {
        key: os.environ[key]
        for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "PATH")
        if key in os.environ
    }
    environment.update(
        APP_ENV="prod",
        FUGA_LOAD_DOTENV="0",
        LOG_LEVEL="WARNING",
        PORT=str(port),
        SUPABASE_URL="https://provider.example.test",
        CORS_ORIGINS="[]",
        DATABASE_URL="postgresql+psycopg://validation:unused@127.0.0.1:1/validation?sslmode=verify-full",
        DATABASE_SSL_ROOT_CERT=str(root / "certs/prod-ca-2021.crt"),
        PYTHONDONTWRITEBYTECODE="1",
    )
    # Fixed local script and current interpreter; no shell or caller-supplied command.
    process = subprocess.Popen(
        [sys.executable, "scripts/start.py"],  # noqa: S603
        cwd=root,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )

    def status(path, timeout=2):
        try:
            # Both path and the loopback origin are fixed by this smoke check.
            with urlopen(f"http://127.0.0.1:{port}{path}", timeout=timeout) as response:  # noqa: S310
                return response.status
        except HTTPError as error:
            return error.code

    try:
        # First imports from a Windows-mounted WSL filesystem can exceed ten seconds.
        # Bound the smoke probe without treating that filesystem cost as an API failure.
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError("El launcher no inició con la configuración de prueba.")
            try:
                if status("/health") == 200:
                    break
            except (OSError, URLError):
                pass
            time.sleep(0.1)
        else:
            raise RuntimeError("No se recibió respuesta del proceso local.")
        expected = {"/health": 200, "/ready": 503, "/docs": 404, "/api/v1/expenses": 401}
        observed = {path: status(path, timeout=10) for path in expected}
        assert observed == expected, "Estado de salud/autorización inesperado"
        print(  # noqa: T201 - Sanitized CLI evidence; no environment values.
            json.dumps(
                {
                    "platform": sys.platform,
                    "python": sys.version.split()[0],
                    "synthetic_config": True,
                    "real_provider_calls": False,
                    "checks": observed,
                }
            )
        )
        return 0
    finally:
        process.terminate()
        process.wait(timeout=10)


if __name__ == "__main__":
    raise SystemExit(main())
