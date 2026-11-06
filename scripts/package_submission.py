"""Build the submission zip from a git ref plus the trained artefacts.

Takes the tracked files of ``--ref`` (default ``origin/main``), adds the model
bundle and k-NN analog library under ``artifacts/`` and writes a zip that runs
without retraining. Self-checks the result: zip integrity, required files
present, no secrets/venvs/caches.

Usage::

    python scripts/package_submission.py --out dist/TyphoonVN_DoAn.zip
"""

from __future__ import annotations

import argparse
import io
import subprocess
import tarfile
import zipfile
from pathlib import Path

ARTIFACT_README = """# Trained artefacts (not in git)

- `model-bundle/` - LSTM trained on IBTrACS WP 1980-2016 (validation 2017-2020),
  checksum-verified, with calibrated 80% cone radii.
- `analog-wp.npz` - k-NN analog library (storms 1980-2020, test storms excluded).

Serve without retraining:

    $env:MODEL_ARTIFACT="artifacts/model-bundle"; $env:ANALOG_ARTIFACT="artifacts/analog-wp.npz"
    python -m uvicorn typhoon_vn.api.app:app

Rebuild from raw data: see "Tai lap ket qua" in docs/report/README.md.
"""
REQUIRED = (
    "README.md",
    "pyproject.toml",
    "docs/report/README.md",
    "docs/acceptance/README.md",
    "artifacts/model-bundle/manifest.json",
    "artifacts/analog-wp.npz",
)
FORBIDDEN = ("node_modules/", ".venv/", "__pycache__/", "/.agent/", "/.vscode/")
EXCLUDE = {"stackhawk.yml"}  # local scanner config, not needed to run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ref", default="origin/main")
    parser.add_argument("--out", type=Path, default=Path("dist/TyphoonVN_DoAn.zip"))
    parser.add_argument(
        "--bundle", type=Path, default=Path("runs/ibtracs-benchmark/bundle")
    )
    parser.add_argument(
        "--analog", type=Path, default=Path("runs/analog/analog-wp.npz")
    )
    args = parser.parse_args(argv)

    for path in (args.bundle / "manifest.json", args.analog):
        if not path.exists():
            raise SystemExit(f"missing artefact: {path}")
    archive = subprocess.run(
        ["git", "archive", "--format=tar", args.ref], check=True, capture_output=True
    ).stdout
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            for member in tar:
                if member.isfile() and member.name not in EXCLUDE:
                    z.writestr(
                        f"TyphoonVN/{member.name}", tar.extractfile(member).read()
                    )
        for file in sorted(args.bundle.rglob("*")):
            if file.is_file():
                relative = file.relative_to(args.bundle).as_posix()
                z.write(file, f"TyphoonVN/artifacts/model-bundle/{relative}")
        z.write(args.analog, "TyphoonVN/artifacts/analog-wp.npz")
        z.writestr("TyphoonVN/artifacts/README.md", ARTIFACT_README)

    with zipfile.ZipFile(args.out) as z:
        assert z.testzip() is None, "corrupt zip"
        names = z.namelist()
    missing = [r for r in REQUIRED if f"TyphoonVN/{r}" not in names]
    junk = [n for n in names if any(f in n for f in FORBIDDEN) or n.endswith("/.env")]
    assert not missing, f"missing from package: {missing}"
    assert not junk, f"unwanted files in package: {junk[:5]}"
    print(
        f"{args.out}: {len(names)} files, {args.out.stat().st_size / 1e6:.1f} MB ({args.ref})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
