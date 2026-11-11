import os
import tempfile
from pathlib import Path


def test_tmpdir_uses_workspace_local_path():
    repo_root = Path(__file__).resolve().parents[1]
    expected = (repo_root / ".pytest-temp").resolve()

    assert Path(tempfile.gettempdir()).resolve() == expected
    assert os.environ.get("TEMP") == str(expected)
    assert os.environ.get("TMP") == str(expected)
    assert os.environ.get("TMPDIR") == str(expected)
