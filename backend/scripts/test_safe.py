"""Run tests with no real dotenv, external HTTP or remote database access."""

import argparse
import os
import socket
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic_settings.sources import DotEnvSettingsSource


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integration", action="store_true")
    parser.add_argument("--coverage", action="store_true")
    args, pytest_args = parser.parse_known_args()
    environment = {
        name: os.environ[name]
        for name in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "PATH")
        if name in os.environ
    }
    environment.update(APP_ENV="test", SUPABASE_URL="https://supabase.example.test")
    if args.integration:
        import psycopg

        dsn = os.environ.get("FUGA_TEST_DATABASE_URL", "")
        try:
            info = psycopg.conninfo.conninfo_to_dict(dsn)
        except Exception:
            parser.error(
                "Se requiere una configuración PostgreSQL local válida, no se muestran valores."
            )
        if info.get("host") not in {"127.0.0.1", "localhost", "::1"} or info.get("hostaddr"):
            parser.error("Solo se permite PostgreSQL local explícito, nunca Supabase.")
        environment["FUGA_TEST_DATABASE_URL"] = dsn

    connect = socket.socket.connect

    def local_connect(sock, address):
        if isinstance(address, tuple) and address[0] in {"127.0.0.1", "::1"}:
            return connect(sock, address)
        raise AssertionError("External network disabled in tests")

    os.chdir(Path(__file__).resolve().parents[1])
    sys.path.insert(0, str(Path.cwd()))
    coverage = None
    if args.coverage:
        from coverage import Coverage

        coverage = Coverage(source=["app"], data_file=".coverage")
        coverage.start()
    with (
        patch.dict(os.environ, environment, clear=True),
        patch.object(DotEnvSettingsSource, "_read_env_files", return_value={}),
        patch("socket.socket.connect", local_connect),
        patch(
            "httpx.HTTPTransport.handle_request", side_effect=AssertionError("Real HTTP disabled")
        ),
    ):
        if args.integration:
            result = pytest.main(["-q", "--tb=short", "-p", "no:cacheprovider", *pytest_args])
        else:
            with (
                patch(
                    "sqlalchemy.create_engine", side_effect=AssertionError("Real database disabled")
                ),
                patch("psycopg.connect", side_effect=AssertionError("Real PostgreSQL disabled")),
            ):
                result = pytest.main(["-q", "--tb=short", "-p", "no:cacheprovider", *pytest_args])
    if coverage:
        coverage.stop()
        coverage.save()
        coverage.report(skip_covered=True)
        coverage.json_report(outfile="docs/coverage.json")
    return result


if __name__ == "__main__":
    sys.exit(main())
