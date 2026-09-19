"""Documentation contract tests for the top-level README."""

import re
from pathlib import Path


def test_readme_local_links_and_safety_claims() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    links = re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
    missing = [
        link
        for link in links
        if not link.startswith(("http://", "https://")) and not Path(link).exists()
    ]
    assert not missing
    assert "not production-ready" in text
    assert "synthetic-demo" in text
    assert "not official weather warnings" in text
    assert "python -m typhoon_vn.cli train --help" in text
