from uuid import uuid4

import httpx
import pytest

from app.core.config import settings
from app.core.errors import AppException, UpstreamException
from app.core.logging import sanitizar_datos
from app.services import profile_photos as photos


@pytest.fixture
def provider(monkeypatch):
    monkeypatch.setattr(settings, "CLOUDINARY_CLOUD_NAME", "local-fixture")
    monkeypatch.setattr(settings, "CLOUDINARY_API_KEY", "local-key")
    monkeypatch.setattr(settings, "CLOUDINARY_API_SECRET", "local-secret")
    return "fuga/" + str(uuid4()) + "/" + uuid4().hex


def asset(pid, **changes):
    return {"public_id": pid, "resource_type": "image", "type": "upload", "format": "png",
            "bytes": 100, "width": 32, "height": 32,
            "secure_url": "https://res.cloudinary.com/local-fixture/image/upload/v1/" + pid + ".png",
            **changes}


@pytest.mark.parametrize("changes,code", [
    ({"bytes": 5_000_001}, 413), ({"bytes": 0}, 400), ({"bytes": "100"}, 400),
    ({"format": "gif"}, 400), ({"width": 0}, 400), ({"height": None}, 400),
    ({"public_id": "another-account"}, 400), ({"resource_type": "video"}, 400),
    ({"secure_url": "https://res.cloudinary.com.evil.invalid/image.png"}, 400),
    ({"secure_url": "https://res.cloudinary.com/other/image/upload/test.png"}, 400),
])
def test_provider_metadata_is_validated(provider, monkeypatch, changes, code):
    def respond(request):
        assert "%2F" in request.url.raw_path.decode()
        return httpx.Response(200, json=asset(provider, **changes))

    monkeypatch.setattr(photos, "cloud_client", lambda: httpx.Client(
        transport=httpx.MockTransport(respond)))
    with pytest.raises(AppException) as error:
        photos.verify_asset(provider)
    assert error.value.status_code == code


def test_provider_network_failure_never_exposes_credentials(provider, monkeypatch):
    def respond(request):
        raise httpx.ConnectError("sensitive provider diagnostic must not escape", request=request)

    monkeypatch.setattr(photos, "cloud_client", lambda: httpx.Client(
        transport=httpx.MockTransport(respond)))
    with pytest.raises(UpstreamException) as error:
        photos.verify_asset(provider)
    assert "diagnostic" not in str(error.value)
    assert "local-secret" not in str(error.value)


def test_valid_asset_and_signed_destroy_use_only_the_registered_id(provider, monkeypatch):
    calls = []

    def respond(request):
        calls.append(request)
        return httpx.Response(200, json=asset(provider) if request.method == "GET"
                              else {"result": "not found"})

    monkeypatch.setattr(photos, "cloud_client", lambda: httpx.Client(
        transport=httpx.MockTransport(respond)))
    assert photos.verify_asset(provider) == asset(provider)["secure_url"]
    assert photos.destroy_asset(provider)
    assert calls[1].url.path.endswith("/image/destroy")
    assert b"invalidate=true" in calls[1].content
    assert b"local-secret" not in calls[1].content


def test_cloudinary_secrets_and_upload_signatures_are_redacted():
    assert sanitizar_datos({"CLOUDINARY_API_SECRET": "server-only",
                           "CLOUDINARY_API_KEY": "server-only", "signature": "temporary"}) == {
        "CLOUDINARY_API_SECRET": "[REDACTED]", "CLOUDINARY_API_KEY": "[REDACTED]",
        "signature": "[REDACTED]"}


def test_signature_matches_official_cloudinary_sha1_example(monkeypatch):
    monkeypatch.setattr(settings, "CLOUDINARY_API_SECRET", "abcd")
    assert photos.signed({"timestamp": 1315060510}) == "a21ad0f63beb4de2e5575204b79ab90bffb02c10"


def test_photo_qa_reads_only_whitelisted_server_fields(monkeypatch):
    from scripts import qa_android

    values = {name: "server-fixture" for name in (
        "CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET")}

    def dotenv(path, *, interpolate):
        assert interpolate is False
        return {**values, "DATABASE_URL": "remote-must-not-enter-qa",
                "SUPABASE_SERVICE_ROLE_KEY": "private-must-not-enter-qa"}

    monkeypatch.setattr(qa_android, "dotenv_values", dotenv)
    assert qa_android.photo_credentials() == values
