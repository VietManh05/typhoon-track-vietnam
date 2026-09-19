"""Package license metadata must match the repository license."""

from importlib.metadata import metadata
from pathlib import Path


def test_mit_license_and_distribution_metadata_agree() -> None:
    text = Path("LICENSE").read_text(encoding="utf-8")
    assert text.startswith("MIT License")
    assert "Copyright (c) 2026 Typhoon VN Forecast System contributors" in text
    assert "Permission is hereby granted, free of charge" in text
    package = metadata("typhoon-vn-forecast-system")
    assert package["License-File"] == "LICENSE"
    assert "License :: OSI Approved :: MIT License" in package.get_all("Classifier", [])
