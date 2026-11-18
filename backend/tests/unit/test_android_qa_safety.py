import pytest

from scripts.qa_android import validate_local_dsn


@pytest.mark.parametrize("dsn", [
    "postgresql://fuga_test@remote.example.test:55440/postgres",
    "postgresql://fuga_test@127.0.0.1:5432/postgres",
    "host=127.0.0.1 hostaddr=192.0.2.1 port=55440 user=fuga_test",
    "postgresql://other@127.0.0.1:55440/postgres",
])
def test_android_qa_rejects_remote_or_unapproved_cluster(dsn):
    with pytest.raises(ValueError):
        validate_local_dsn(dsn)


def test_android_qa_accepts_only_its_explicit_loopback_cluster():
    assert validate_local_dsn(
        "postgresql://fuga_test@127.0.0.1:55440/postgres"
    )["host"] == "127.0.0.1"
