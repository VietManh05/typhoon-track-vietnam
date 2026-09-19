"""Configure the approved DVC remote supplied by the operator environment."""

from __future__ import annotations

import os
import subprocess


def main() -> int:
    url = os.environ.get("DVC_REMOTE_URL")
    if not url:
        raise SystemExit("DVC_REMOTE_URL is required; no remote was changed")
    subprocess.run(
        ["dvc", "remote", "add", "--local", "--force", "-d", "storage", url],
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
