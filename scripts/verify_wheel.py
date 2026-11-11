"""Install a built wheel without dependencies and smoke-test it outside the repo.

Usage: python scripts/verify_wheel.py path/to/package.whl
Dependencies must already exist in the invoking interpreter. No production DB is used.
"""

import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    wheel = Path(sys.argv[1]).resolve(strict=True)
    root = Path(__file__).resolve().parents[1] / ".pytest-temp"
    root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wheel-smoke-", dir=root) as directory:
        work = Path(directory)
        installed = work / "installed"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--no-compile",
                "--target",
                str(installed),
                str(wheel),
            ],
            check=True,
            cwd=work,
        )
        program = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from typhoon_vn.operations import store as module
assert Path(module.__file__).is_relative_to(Path(sys.argv[1]))
root = Path(module.__file__).parent
assert (root / 'migrations/versions/0001_operational_schema.py').is_file()
assert (root / 'legacy_migrations/versions/0002_import.py').is_file()
for url in ('sqlite:///:memory:', 'sqlite:///wheel-smoke.db'):
    store = module.Store(url)
    assert store.active() == []
    store.engine.dispose()
print('Installed wheel: packaged migrations and external-cwd Store startup PASS')
"""
        subprocess.run(
            [sys.executable, "-I", "-c", program, str(installed)], check=True, cwd=work
        )


if __name__ == "__main__":
    main()
