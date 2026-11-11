"""Auditable local backup and restore helpers for Phase 6 drills."""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, slots=True)
class BackupManifest:
    artifact_type: str
    source: str
    backup_path: str
    sha256: str
    created_at: str
    bytes: int

    def write(self, path: Path) -> Path:
        path.write_text(
            json.dumps(asdict(self), indent=2, sort_keys=True), encoding="utf-8"
        )
        return path

    @classmethod
    def read(cls, path: Path) -> "BackupManifest":
        return cls(**json.loads(path.read_text(encoding="utf-8")))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class BackupManager:
    """File-based backup manager used by CI restore drills and runbooks."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def backup_file(self, source: Path, *, artifact_type: str) -> BackupManifest:
        source = Path(source)
        if not source.is_file():
            raise FileNotFoundError(source)
        if artifact_type not in {"database", "model", "config"}:
            raise ValueError("unsupported artifact_type")
        digest = sha256_file(source)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        target = (
            self.root
            / artifact_type
            / f"{source.stem}-{stamp}-{digest[:12]}{source.suffix}"
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".tmp")
        shutil.copy2(source, tmp)
        tmp.replace(target)
        manifest = BackupManifest(
            artifact_type=artifact_type,
            source=str(source),
            backup_path=str(target),
            sha256=digest,
            created_at=datetime.now(timezone.utc).isoformat(),
            bytes=target.stat().st_size,
        )
        manifest.write(target.with_suffix(target.suffix + ".manifest.json"))
        return manifest

    def restore_file(self, manifest: BackupManifest, target: Path) -> Path:
        backup = Path(manifest.backup_path)
        if not backup.is_file():
            raise FileNotFoundError(backup)
        actual = sha256_file(backup)
        if actual != manifest.sha256:
            raise ValueError("backup checksum mismatch")
        target = Path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".restore.tmp")
        shutil.copy2(backup, tmp)
        tmp.replace(target)
        return target
