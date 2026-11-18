from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import UpstreamException
from app.services import profile_photos as photos

pytestmark = pytest.mark.integration


@pytest.fixture
def cloud(monkeypatch):
    monkeypatch.setattr(settings, "CLOUDINARY_CLOUD_NAME", "local-fixture")
    monkeypatch.setattr(settings, "CLOUDINARY_API_KEY", "local-key")
    monkeypatch.setattr(settings, "CLOUDINARY_API_SECRET", "local-secret")
    monkeypatch.setattr(photos, "verify_asset", lambda pid:
                        "https://res.cloudinary.com/local-fixture/image/upload/v1/" + pid + ".png")


def account(database, signer):
    uid = uuid4()
    database.execute(text("INSERT INTO auth.users(id,email) VALUES (:id,'qa@local.invalid')"),
                     {"id": uid})
    database.commit()
    return uid, {"Authorization": "Bearer " + signer(sub=str(uid))}


def issue(client, headers):
    response = client.post("/api/v1/me/photo/signature", headers=headers)
    assert response.status_code == 200
    assert "local-secret" not in response.text
    data = response.json()
    assert data["overwrite"] == "false"
    assert data["allowed_formats"] == "jpg,jpeg,png,webp"
    assert data["signature"] == photos.signed({key: data[key] for key in (
        "timestamp", "public_id", "overwrite", "allowed_formats")})
    return data["public_id"]


def complete(client, headers, pid):
    return client.post("/api/v1/me/photo/complete", headers=headers, json={"public_id": pid})


def test_photo_persists_on_fresh_session_and_replacements_are_idempotent(
    integrated_client, database, signer, cloud,
):
    uid, headers = account(database, signer)
    first = issue(integrated_client, headers)
    response = complete(integrated_client, headers, first)
    assert response.status_code == 200
    url = response.json()["foto_url"]
    assert database.execute(text("SELECT foto_url FROM perfil WHERE id=:id"),
                            {"id": uid}).scalar_one() == url
    fresh_headers = {"Authorization": "Bearer " + signer(sub=str(uid))}
    assert integrated_client.get("/api/v1/me", headers=fresh_headers).json()["foto_url"] == url
    assert complete(integrated_client, fresh_headers, first).json()["foto_url"] == url
    second = issue(integrated_client, headers)
    assert complete(integrated_client, headers, second).status_code == 200
    assert complete(integrated_client, headers, first).status_code == 400
    assert database.execute(text("SELECT estado FROM perfil_foto_carga WHERE public_id=:pid"),
                            {"pid": first}).scalar_one() == "retirada"


def test_cancel_expiration_foreign_and_unregistered_assets_cannot_replace_photo(
    integrated_client, database, signer, cloud,
):
    uid, headers = account(database, signer)
    _, other = account(database, signer)
    pid = issue(integrated_client, headers)
    assert complete(integrated_client, other, pid).status_code == 403
    assert complete(integrated_client, headers, f"fuga/{uid}/{uuid4().hex}").status_code == 400
    response = integrated_client.post("/api/v1/me/photo/cancel", headers=headers,
                                      json={"public_id": pid})
    assert response.json()["estado"] == "cancelada"
    assert complete(integrated_client, headers, pid).status_code == 400
    expired = issue(integrated_client, headers)
    database.execute(text("UPDATE perfil_foto_carga SET created_at=now()-interval '2 hours' "
                          "WHERE public_id=:pid"), {"pid": expired})
    database.commit()
    assert complete(integrated_client, headers, expired).status_code == 400
    assert integrated_client.get("/api/v1/me", headers=headers).json()["foto_url"] is None


def test_failure_keeps_previous_photo_and_retry_can_finish(
    integrated_client, database, signer, cloud, monkeypatch,
):
    _, headers = account(database, signer)
    first = issue(integrated_client, headers)
    previous = complete(integrated_client, headers, first).json()["foto_url"]
    next_id = issue(integrated_client, headers)
    verify = photos.verify_asset

    def unavailable(_):
        raise UpstreamException("Proveedor temporalmente no disponible.")

    monkeypatch.setattr(photos, "verify_asset", unavailable)
    assert complete(integrated_client, headers, next_id).status_code == 503
    assert integrated_client.get("/api/v1/me", headers=headers).json()["foto_url"] == previous
    monkeypatch.setattr(photos, "verify_asset", verify)
    assert complete(integrated_client, headers, next_id).status_code == 200
    # A cancel received after successful completion must not clear the active photo.
    assert integrated_client.post("/api/v1/me/photo/cancel", headers=headers,
                                   json={"public_id": next_id}).json()["estado"] == "activa"


def test_cleanup_dry_run_grace_references_and_retry_are_safe(
    integrated_client, database, signer, cloud, monkeypatch,
):
    uid, headers = account(database, signer)
    other_uid, other = account(database, signer)
    old = issue(integrated_client, headers)
    complete(integrated_client, headers, old)
    current = issue(integrated_client, headers)
    complete(integrated_client, headers, current)
    abandoned = issue(integrated_client, headers)
    other_current = issue(integrated_client, other)
    complete(integrated_client, other, other_current)
    calls = []
    monkeypatch.setattr(photos, "destroy_asset", lambda pid: calls.append(pid) or True)
    # Only this user's attempts are aged; a current asset is still ineligible.
    database.execute(text("UPDATE perfil_foto_carga SET updated_at=now()-interval '3 hours' "
                          "WHERE usuario_id=:uid"), {"uid": uid})
    database.commit()
    summary = photos.cleanup_uploads(database)
    assert summary["dry_run"] and not calls
    # Protect even an asset erroneously referenced by a different profile.
    old_url = photos.verify_asset(old)
    database.execute(text("UPDATE perfil SET foto_url=:url WHERE id=:uid"),
                     {"uid": other_uid, "url": old_url})
    database.commit()
    photos.cleanup_uploads(database, apply=True)
    assert abandoned in calls and old not in calls and current not in calls
    assert other_current not in calls
    database.execute(text("UPDATE perfil SET foto_url=NULL WHERE id=:uid"), {"uid": other_uid})
    database.commit()
    monkeypatch.setattr(photos, "destroy_asset", lambda pid: False)
    photos.cleanup_uploads(database, apply=True)
    assert database.execute(text("SELECT estado FROM perfil_foto_carga WHERE public_id=:pid"),
                            {"pid": old}).scalar_one() == "retirada"
    monkeypatch.setattr(photos, "destroy_asset", lambda pid: calls.append(pid) or True)
    photos.cleanup_uploads(database, apply=True)
    assert old in calls
    assert complete(integrated_client, headers, old).status_code == 400


def test_concurrent_completion_serializes_per_profile(
    integrated_client, database, signer, cloud, postgres_engine,
):
    uid, headers = account(database, signer)
    ids = [issue(integrated_client, headers) for _ in range(2)]

    def finish(pid):
        with Session(postgres_engine) as db:
            photos.complete_upload(db, uid, pid)

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(finish, ids))
    assert database.execute(text("SELECT count(*) FROM perfil_foto_carga "
                                 "WHERE usuario_id=:uid AND estado='activa'"),
                            {"uid": uid}).scalar_one() == 1


def test_upload_registry_denies_client_sql_access(database):
    database.execute(text("SET LOCAL ROLE authenticated"))
    with pytest.raises(ProgrammingError), database.begin_nested():
        database.execute(text("SELECT * FROM public.perfil_foto_carga"))
    database.rollback()


def test_database_failure_rolls_back_url_and_attempt_states(
    integrated_client, database, signer, cloud, postgres_engine, monkeypatch,
):
    uid, headers = account(database, signer)
    previous_id = issue(integrated_client, headers)
    previous_url = complete(integrated_client, headers, previous_id).json()["foto_url"]
    new_id = issue(integrated_client, headers)

    def failed_commit():
        raise SQLAlchemyError("synthetic local failure")

    with Session(postgres_engine) as transaction:
        monkeypatch.setattr(transaction, "commit", failed_commit)
        with pytest.raises(SQLAlchemyError):
            photos.complete_upload(transaction, uid, new_id)
    assert integrated_client.get("/api/v1/me", headers=headers).json()["foto_url"] == previous_url
    assert database.execute(text("SELECT estado FROM perfil_foto_carga WHERE public_id=:pid"),
                            {"pid": new_id}).scalar_one() == "pendiente"


def test_signature_rate_limit_is_scoped_to_the_authenticated_user(
    integrated_client, database, signer, cloud,
):
    _, headers = account(database, signer)
    for _ in range(10):
        issue(integrated_client, headers)
    assert integrated_client.post("/api/v1/me/photo/signature", headers=headers).status_code == 429
    _, other = account(database, signer)
    issue(integrated_client, other)
