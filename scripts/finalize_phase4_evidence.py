"""Record the verified Phase 4 state without hiding the real PostGIS blocker."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "docs" / "planning"
EVIDENCE = PLANNING / "evidence"
DATE = "2026-09-19"
FOCUSED = (
    ".venv/Scripts/python.exe -m pytest tests/test_phase4_backend.py "
    "tests/test_inference_api.py tests/test_cache.py -q"
)
REGRESSION = ".venv/Scripts/python.exe -m pytest -q"

GROUPS = {
    16: (
        "Dịch vụ inference",
        "complete",
        "Load bundle một lần, shared scaler/schema, direct multi-horizon, output vật lý/provenance, cache thread-safe và fallback có cờ/lý do/log.",
    ),
    17: (
        "FastAPI",
        "in_progress",
        "Endpoint, schema, OpenAPI, request ID, 401/404/422/429/503 và Redis/DB path đã pass local; gate chờ G18/PostGIS thật.",
    ),
    18: (
        "Database, PostGIS và migration",
        "in_progress",
        "Alembic upgrade/downgrade SQLite, tám bảng, audit/FK/unique/index và migration PostGIS/GiST đã có; chưa chạy được test PostGIS thật.",
    ),
    19: (
        "Worker thời gian thực",
        "in_progress",
        "Provider protocol, validate-before-write, revision idempotency, forecast persistence/cache, bounded exponential retry và status đã pass local; gate chờ G17/G20.",
    ),
    20: (
        "Redis và invalidation",
        "in_progress",
        "Read/write/TTL/hit/miss/fail-open, active/forecast response cache và invalidation theo storm/model đã pass bằng fake Redis; gate chờ G17.",
    ),
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def update_group_header(group: int, status: str, evidence_file: str) -> None:
    path = PLANNING / f"wbs-{group:02d}.md"
    text = path.read_text(encoding="utf-8-sig")
    replacement = (
        f"- Trạng thái: {status}; bằng chứng tại "
        f"[{evidence_file}](evidence/{evidence_file})."
    )
    text = text.replace("- Trạng thái: pending; chưa nghiệm thu.", replacement, 1)
    write(path, text)


def complete_g16_tasks(catalog: dict) -> None:
    path = PLANNING / "wbs-16.md"
    text = path.read_text(encoding="utf-8-sig")
    tasks = [task for task in catalog["tasks"] if task["group"] == 16]
    if len(tasks) != 20:
        raise RuntimeError(f"expected 20 G16 tasks, found {len(tasks)}")
    for task in tasks:
        task["status"] = "complete"
        marker = f'<a id="{task["anchor"]}"></a>'
        start = text.index(marker)
        end = text.find('<a id="', start + len(marker))
        if end < 0:
            end = len(text)
        block = text[start:end]
        block = block.replace(
            "- **Trạng thái:** pending.", "- **Trạng thái:** complete.", 1
        )
        block = block.replace(
            "- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.",
            f'- **Bằng chứng hiện tại:** [{task["id"]}.md](evidence/{task["id"]}.md).',
            1,
        )
        text = text[:start] + block + text[end:]
        write(
            EVIDENCE / f"{task['id']}.md",
            f"""# {task['id']} — {task['title']}

- **Trạng thái:** complete ({DATE}).
- **Expected:** contract “{task['title']}” tại `{task['file']}#{task['anchor']}` đạt case thường, biên và failure-mode liên quan.
- **Actual:** implementation được kiểm chứng trong service/bundle/schema/fallback/thread-safety; focused **20 passed**, exit 0; regression **148 passed, 1 skipped**, exit 0.
- **Lệnh focused:** `{FOCUSED}`.
- **Evidence nhóm:** [G16-inference.md](G16-inference.md).
- **Giới hạn:** fixture local/synthetic xác nhận contract phần mềm, không phải skill khí tượng production.
""",
        )
    write(path, text)


def update_supplemental(catalog: dict) -> None:
    path = PLANNING / "supplemental_tasks.md"
    text = path.read_text(encoding="utf-8-sig")
    records = {item["id"]: item for item in catalog["supplemental_tasks"]}
    states = {
        "S09": (
            "in_progress",
            "Cone/province/coast overlap và boundary-touch đã pass local; spatial query PostGIS/UI limitation còn chờ G18/G21.",
        ),
        "S15": (
            "in_progress",
            "Lịch UTC mùa 6–11, ngoài mùa theo thứ Hai, year-boundary và bounded backfill đã pass; gate chờ G19.",
        ),
        "S24": (
            "complete",
            "CLI raw→clean→features ghi provenance/hash/config, bảo toàn raw input và fail nonzero khi path/config sai.",
        ),
    }
    for identifier, (status, actual) in states.items():
        record = records[identifier]
        record["status"] = status
        record["evidence"] = f"evidence/{identifier}.md"
        marker = f'<a id="{record["anchor"]}"></a>'
        start = text.index(marker)
        end = text.find('<a id="', start + len(marker))
        if end < 0:
            end = len(text)
        block = text[start:end]
        block = block.replace(
            "- **Trạng thái:** pending.", f"- **Trạng thái:** {status}.", 1
        )
        block = block.replace(
            f"- **Bằng chứng:** evidence/{identifier}.md — chưa thực hiện.",
            f"- **Bằng chứng:** [{identifier}.md](evidence/{identifier}.md).",
            1,
        )
        text = text[:start] + block + text[end:]
        write(
            EVIDENCE / f"{identifier}.md",
            f"""# {identifier} — Phase 4 supplemental evidence

- **Trạng thái:** {status} ({DATE}).
- **Actual:** {actual}
- **Kiểm chứng:** `{FOCUSED}` → **20 passed**, exit 0.
- **Regression:** `{REGRESSION}` → **148 passed, 1 skipped**, exit 0.
- **Blocker nếu còn:** PostGIS thật cần `POSTGIS_TEST_URL`; Docker không có trong môi trường hiện tại.
""",
        )
    write(path, text)


def main() -> None:
    catalog_path = PLANNING / "task_catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    complete_g16_tasks(catalog)
    for group, (title, status, actual) in GROUPS.items():
        evidence_file = f"G{group:02d}-{['inference', 'api', 'database', 'worker', 'cache'][group - 16]}.md"
        update_group_header(group, status, evidence_file)
        write(
            EVIDENCE / evidence_file,
            f"""# G{group:02d} — {title}

- **Ngày:** {DATE}.
- **Trạng thái:** {status}.
- **Actual:** {actual}
- **Focused:** **20 passed**, exit 0 (`phase4-focused-pytest.xml`).
- **Coverage:** **83%** trên module Phase 4 (`phase4-coverage.xml`).
- **Regression:** **148 passed, 1 skipped**, exit 0 (`phase4-regression-pytest.xml`).
- **Skip duy nhất:** `tests/integration/test_postgis.py` cần `POSTGIS_TEST_URL`; máy hiện tại không có Docker executable.
- **Quality:** flake8 toàn `src tests migrations`, Black toàn phạm vi và compileall đều pass; isort riêng file Phase 4 pass.
""",
        )
    update_supplemental(catalog)
    write(
        EVIDENCE / "PHASE-4.md",
        f"""# Phase 4 — Backend M3

- **Ngày:** {DATE}.
- **Phạm vi:** G16–G20 và S09/S15/S24.
- **Hoàn tất:** G16 và S24.
- **Local-ready nhưng chưa đóng gate:** G17/G18/G19/G20, S09/S15.
- **Focused:** **20 passed**, coverage **83%**, exit 0.
- **Regression:** **148 passed, 1 skipped**, exit 0.
- **Blocker duy nhất:** chưa có Docker hoặc `POSTGIS_TEST_URL` để chạy migration/constraint/SRID/GiST trên PostGIS thật. Migration và test tích hợp đã được chuẩn bị tại `migrations/versions/0001_operational_schema.py` và `tests/integration/test_postgis.py`.
- **Không tuyên bố:** Phase 4 complete hoặc production-ready trước khi test PostGIS thật pass và các gate phụ thuộc được đóng.
""",
    )
    write(catalog_path, json.dumps(catalog, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
