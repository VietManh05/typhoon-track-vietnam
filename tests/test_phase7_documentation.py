from pathlib import Path

DOCS = [
    "docs/model-card.md",
    "docs/user-guide.md",
    "docs/acceptance/phase7-acceptance.md",
    "docs/acceptance/phase7-demo.md",
    "docs/acceptance/project-dod.md",
    "docs/post-season-report.md",
    "docs/handover-slides.md",
]


def test_phase7_docs_exist_with_version_and_safety_boundary():
    for doc in DOCS:
        text = Path(doc).read_text(encoding="utf-8")
        assert "0.1.0-phase7-local" in text
        assert (
            "not an official warning system" in text.lower()
            or "pending" in text.lower()
        )


def test_a29_coverage_and_metrics():
    text = Path("docs/acceptance/project-dod.md").read_text(encoding="utf-8")
    for i in range(1, 29):
        assert f"A29-{i:03d}" in text
    assert "+6/+12/+24/+48/+72" in text
    assert "km" in text or "kilometres" in text


def test_demo_surfaces():
    text = Path("docs/acceptance/phase7-demo.md").read_text(encoding="utf-8").lower()
    for term in [
        "data",
        "model",
        "+6h",
        "dashboard",
        "api",
        "worker",
        "alerts",
        "faketransport",
        "throttle",
    ]:
        assert term in text
