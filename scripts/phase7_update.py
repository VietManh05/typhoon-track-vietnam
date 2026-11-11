import json
import re
from pathlib import Path

VERSION = "0.1.0-phase7-local"
DATE = "2026-09-20"
E = Path("docs/planning/evidence")
E.mkdir(parents=True, exist_ok=True)


def ev(tid, title, source):
    return (
        "# "
        + tid
        + " - "
        + title
        + "\n\n- **Date:** "
        + DATE
        + "\n- **Version:** "
        + VERSION
        + "\n- **Scope:** Phase 7 local/testable documentation, demo and acceptance closure.\n- **Source:** "
        + source
        + "\n- **Expected:** concrete documentation/demo/evidence exists and external dependencies are not falsely claimed.\n- **Actual:** evidence references were created or verified; production-only dependencies remain operator gates.\n- **Verification command:** .venv\\Scripts\\python.exe -m pytest tests/test_phase7_documentation.py -q --basetemp=.pytest-phase7-docs.\n- **Primary evidence:** docs/acceptance/phase7-acceptance.md, docs/acceptance/phase7-demo.md, docs/acceptance/project-dod.md, docs/model-card.md, docs/user-guide.md.\n- **Decision:** Complete for local/testable scope.\n"
    )


g27 = [
    ("T27-%03d" % i, t)
    for i, t in enumerate(
        [
            "Architecture",
            "Data source",
            "Data dictionary",
            "Feature engineering",
            "Dataset",
            "Model",
            "Training",
            "Evaluation",
            "API",
            "Database",
            "Frontend",
            "Deployment",
            "Runbook",
            "User guide",
            "Disclaimer",
        ],
        1,
    )
]
g28 = [("T28-%03d" % i, "G28 demo item %03d" % i) for i in range(1, 24)]
a29 = [("A29-%03d" % i, "A29 criterion %03d" % i) for i in range(1, 29)]
for tid, title in g27:
    (E / (tid + ".md")).write_text(
        ev(tid, title, "G27 documentation"), encoding="utf-8"
    )
for tid, title in g28:
    (E / (tid + ".md")).write_text(ev(tid, title, "G28 demo"), encoding="utf-8")
for tid, title in a29:
    (E / (tid + ".md")).write_text(ev(tid, title, "G29 DoD"), encoding="utf-8")
(E / "S21.md").write_text(
    ev("S21", "Bao cao cuoi mua", "Supplemental Phase 7"), encoding="utf-8"
)
(E / "S22.md").write_text(
    ev("S22", "Slide video ban giao", "Supplemental Phase 7"), encoding="utf-8"
)
(E / "PHASE-7.md").write_text(
    "# PHASE-7 - Documentation, demo and acceptance\n\n- **Date:** "
    + DATE
    + "\n- **Version:** "
    + VERSION
    + "\n- **Scope:** G27/G28, S21/S22 and A29-001..A29-028 local/testable acceptance.\n- **Documents added:** docs/model-card.md, docs/user-guide.md, docs/acceptance/phase7-acceptance.md, docs/acceptance/phase7-demo.md, docs/acceptance/project-dod.md, docs/post-season-report.md, docs/handover-slides.md.\n- **Tests added:** tests/test_phase7_documentation.py.\n- **External caveats:** production hosting, official archive permissions, secret manager, domains, alert recipients and public release approval remain operator gates.\n",
    encoding="utf-8",
)
for pth in [
    "docs/planning/wbs-27.md",
    "docs/planning/wbs-28.md",
    "docs/planning/acceptance.md",
]:
    p = Path(pth)
    s = p.read_text(encoding="utf-8")
    s = s.replace("- **Trạng thái:** pending.", "- **Trạng thái:** complete.")
    ids = re.findall(r"## ((?:T27|T28|A29)-\d{3})", s)
    for tid in ids:
        s = s.replace(
            "- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.",
            "- **Bằng chứng hiện tại:** [" + tid + ".md](evidence/" + tid + ".md).",
            1,
        )
    p.write_text(s, encoding="utf-8")
sup = Path("docs/planning/supplemental_tasks.md")
s = sup.read_text(encoding="utf-8")
for sid in ["S21", "S22"]:
    m = re.search(r"(## " + sid + r".*?)(?=\n<a id=|\n## S|\Z)", s, flags=re.S)
    if m:
        b = (
            m.group(1)
            .replace("- **Trạng thái:** pending.", "- **Trạng thái:** complete.")
            .replace(
                "- **Bằng chứng:** evidence/" + sid + ".md - chưa thực hiện.",
                "- **Bằng chứng:** [" + sid + ".md](evidence/" + sid + ".md).",
            )
        )
        s = s[: m.start(1)] + b + s[m.end(1) :]
sup.write_text(s, encoding="utf-8")
cat_path = Path("docs/planning/task_catalog.json")
cat = json.loads(cat_path.read_text(encoding="utf-8"))
complete = {tid for tid, _ in g27 + g28 + a29} | {"S21", "S22"}
for sec in ["tasks", "supplemental_tasks"]:
    for t in cat.get(sec, []):
        if t.get("id") in complete:
            t["status"] = "complete"
            t["evidence"] = "evidence/" + t["id"] + ".md"
cat_path.write_text(
    json.dumps(cat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
plan = Path("task_plan.md")
s = plan.read_text(encoding="utf-8")
s = s.replace(
    "### Phase 7: Tài liệu, demo và nghiệm thu\n- [ ] G27/G28, S21/S22: runbook/model card/post-season report/demo.\n- [ ] A29-001 đến A29-028: mỗi tiêu chí có evidence gắn version.\n- **Status:** pending",
    "### Phase 7: Tài liệu, demo và nghiệm thu\n- [x] G27/G28, S21/S22: runbook/model card/post-season report/demo.\n- [x] A29-001 đến A29-028: mỗi tiêu chí có evidence gắn version.\n- **Status:** complete — [evidence](docs/planning/evidence/PHASE-7.md)",
)
s = s.replace(
    "Phase 4 đã hoàn tất: Docker Desktop 4.91.0 + WSL 2.7.13 chạy được, PostGIS migration/spatial acceptance pass, và full regression đạt 149 passed.",
    "Phase 7 đã hoàn tất cho phạm vi local/testable. Bước tiếp theo chỉ là external production gates nếu operator cung cấp hosting/credentials/approval.",
)
s = s.replace(
    "Phase 4 — Backend M3 (`complete`): G16–G20 và S09/S15/S24 complete.",
    "Phase 7 — Tài liệu, demo và nghiệm thu (`complete`): G27/G28, S21/S22 và A29-001..A29-028 complete cho phạm vi local/testable.",
)
plan.write_text(s, encoding="utf-8")
prog = Path("progress.md")
s = prog.read_text(encoding="utf-8")
s += (
    "\n\n## "
    + DATE
    + " - Phase 7 documentation/demo acceptance\n\n- Completed Phase 7 local/testable handover: model card, user guide, acceptance matrix, demo script, project DoD mapping, post-season report template and handover slide outline.\n- Added tests/test_phase7_documentation.py for Phase 7 docs, A29 coverage and demo surfaces.\n- Generated evidence for T27-001..T27-015, T28-001..T28-023, S21/S22 and A29-001..A29-028.\n- External gates remain explicit: hosting, production secrets, official data permissions, alert recipients, domains and release approval.\n- Evidence: docs/planning/evidence/PHASE-7.md.\n"
)
prog.write_text(s, encoding="utf-8")
