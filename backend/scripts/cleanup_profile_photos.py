"""HU-08: dry-run by default; --apply explicitly enables Cloudinary deletion.

Run only against the approved database. Never prints asset IDs, URLs or credentials.
Requires migration 0010. Old/untracked assets and current photos are never deleted.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--qa-local", action="store_true",
                        help="Usa solo la base QA de fotografías local, nunca Supabase.")
    args = parser.parse_args()
    if args.qa_local:
        from scripts.qa_android import ROOT, photo_credentials

        state = json.loads((ROOT / ".tools/android-qa/state-photos.json").read_text())
        name = state.get("database", "")
        if not re.fullmatch(r"fuga_android_qa_[0-9a-f]{32}", name):
            raise ValueError("La sesión QA no está activa.")
        cloud = photo_credentials()
        utility = {key: value for key, value in os.environ.items()
                   if key.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP"}}
        os.environ.clear()
        os.environ.update(utility)
        os.environ.update(cloud)
        os.environ.update(APP_ENV="test", FUGA_LOAD_DOTENV="0", LOG_LEVEL="WARNING",
                          DATABASE_URL="postgresql+psycopg://fuga_test@127.0.0.1:55440/" + name)
    from sqlalchemy.orm import Session

    from app.db.session import get_engine
    from app.services.profile_photos import cleanup_uploads

    engine = get_engine()
    try:
        with Session(engine) as db:
            print(json.dumps(cleanup_uploads(db, apply=args.apply, limit=args.limit)))
    finally:
        engine.dispose()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("No se pudo completar la limpieza de fotografías; no se muestran datos.",
              file=sys.stderr)
        sys.exit(1)
