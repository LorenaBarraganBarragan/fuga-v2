import logging

from app.core.logging import SensitiveFilter, setup_logging


def test_access_log_removes_query_search_personal_data():
    record = logging.LogRecord(
        "uvicorn.access",
        logging.INFO,
        "",
        0,
        '%s - "%s %s HTTP/%s" %s',
        ("127.0.0.1", "GET", "/api/v1/admin/users?q=student%40example.test", "1.1", 200),
        None,
    )
    SensitiveFilter().filter(record)
    assert record.args[2] == "/api/v1/admin/users"
    assert "student" not in record.getMessage()


def test_uvicorn_own_handlers_are_protected():
    setup_logging()
    assert any(
        isinstance(item, SensitiveFilter) for item in logging.getLogger("uvicorn.access").filters
    )
