"""Create a source-only demo handover archive without local secrets or runtime data."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "typhoon-vn-demo-source-2026-09-23.zip"
ROOT_FILES = (
    ".env.example",
    "LICENSE",
    "README.md",
    "alembic.ini",
    "conftest.py",
    "docker-compose.preview.yml",
    "docker-compose.prod.yml",
    "docker-compose.share.yml",
    "docker-compose.yml",
    "pyproject.toml",
    "requirements-api.txt",
    "requirements-ingestion.txt",
    "requirements-train.txt",
    "requirements.txt",
)
DIRECTORIES = ("src", "tests", "migrations", "infra", "scripts")
FRONTEND_PARTS = (
    "functions",
    "public",
    "src",
    "tests",
    "scripts",
    "index.html",
    "package.json",
    "package-lock.json",
    "postcss.config.js",
    "tailwind.config.js",
    "tsconfig.json",
    "vite.config.ts",
)
DOC_FILES = (
    "docs/deployment.md",
    "docs/model-card.md",
    "docs/nchmf.md",
    "docs/runbook.md",
    "docs/user-guide.md",
    "reports/handover-remediation-2026-09-23.md",
    "reports/demo-release-smoke-2026-09-23.json",
    "reports/demo-ui-smoke-2026-09-23.json",
    "reports/demo-uat-checklist-2026-09-23.md",
)
EXCLUDED_PARTS = {
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".wrangler",
    ".venv",
    "secrets",
}
ALLOWED_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".png",
    ".ps1",
    ".py",
    ".svg",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".woff2",
    ".yaml",
    ".yml",
}


def included_files() -> list[Path]:
    candidates = [ROOT / name for name in ROOT_FILES]
    candidates += [ROOT / name for name in DOC_FILES]
    for directory in DIRECTORIES:
        candidates += list((ROOT / directory).rglob("*"))
    for part in FRONTEND_PARTS:
        path = ROOT / "viz" / "frontend" / part
        candidates += list(path.rglob("*")) if path.is_dir() else [path]
    files = []
    for path in candidates:
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(ROOT)
        if any(
            part in EXCLUDED_PARTS or part.startswith(".env.")
            for part in relative.parts
        ):
            if relative.as_posix() != ".env.example":
                continue
        if path.suffix not in ALLOWED_SUFFIXES:
            continue
        files.append(path)
    return sorted(set(files), key=lambda item: item.relative_to(ROOT).as_posix())


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    manifest = []
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in included_files():
            relative = path.relative_to(ROOT).as_posix()
            content = path.read_bytes()
            archive.writestr(relative, content)
            manifest.append(
                {
                    "path": relative,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "bytes": len(content),
                }
            )
        archive.writestr(
            "HANDOVER-MANIFEST.json", json.dumps(manifest, indent=2) + "\n"
        )
    with ZipFile(OUTPUT) as archive:
        recorded = json.loads(archive.read("HANDOVER-MANIFEST.json"))
        assert recorded == manifest
        assert len(archive.namelist()) == len(manifest) + 1
        for entry in manifest:
            assert (
                hashlib.sha256(archive.read(entry["path"])).hexdigest()
                == entry["sha256"]
            )
    print(f"Created {OUTPUT} with {len(manifest)} source files")
    print(f"SHA-256: {hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
