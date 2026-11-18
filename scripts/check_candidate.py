"""Inspect a candidate without staging files, reading dotenv or printing secret values."""

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "supabase_secret": re.compile(r"\bsb_secret_[A-Za-z0-9_-]{24,}\b"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    files = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        text=True,
    ).split("\0")
    issues = []
    manifest = []
    for name in sorted(set(filter(None, files))):
        path = ROOT / name
        if not path.is_file() or path == args.output:
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            issues.append({"file": name, "issue": "nonexample_environment_file"})
            continue
        manifest.append(name)
        if path.suffix not in {
            ".py",
            ".ts",
            ".tsx",
            ".cjs",
            ".js",
            ".json",
            ".yaml",
            ".yml",
            ".md",
            ".example",
            ".sql",
            ".toml",
            ".lock",
            ".ps1",
            ".sh",
            ".xml",
            ".crt",
            ".pem",
        }:
            continue
        content = path.read_text(encoding="utf-8-sig")
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(content):
                issues.append(
                    {
                        "file": name,
                        "line": content.count("\n", 0, match.start()) + 1,
                        "issue": label,
                    }
                )
    result = {
        "scope": "current tracked and nonignored candidate files; not full Git history or APK",
        "files": manifest,
        "issues_without_values": issues,
    }
    if args.output:
        target = args.output.resolve()
        if not target.is_relative_to(ROOT / "mi-framework-ia" / "docs" / "auditoria"):
            parser.error("El inventario solo se escribe dentro de docs/auditoria.")
        target.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(
        json.dumps(
            {"files_checked": len(manifest), "issues_without_values": issues},
            ensure_ascii=False,
        )
    )
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
