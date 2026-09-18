"""Validate planning structure without touching product code or running training."""
from pathlib import Path
import ast
import hashlib
import json
import re

root = Path.cwd()
out = root / "docs/planning"
catalog = json.loads((out / "task_catalog.json").read_text(encoding="utf-8"))
source = root / catalog["source_file"]
errors = []
def check(ok, message):
    if not ok:
        errors.append(message)

check(hashlib.sha256(source.read_bytes()).hexdigest() == catalog["source_sha256"],
      "Source roadmap hash changed")
lines = source.read_text(encoding="utf-8").splitlines()
expected = {i for i, line in enumerate(lines, 1) if re.match(r"^- \[[ xX]\]", line)}
source_items = catalog["requirements"] + catalog["tasks"]
actual = [r["line"] for r in source_items]
check(set(actual) == expected, "Source checkbox coverage differs")
check(len(actual) == len(set(actual)), "Duplicate source mapping")
all_tasks = catalog["tasks"] + catalog["supplemental_tasks"] + catalog["priority_tasks"]
ids = [r["id"] for r in all_tasks]
check(len(ids) == len(set(ids)), "Duplicate task IDs")
groups = json.loads((out / "tools/groups.json").read_text(encoding="utf-8-sig"))
graph = {f"G{g[0]:02d}": re.findall(r"G\d{2}", g[3]) for g in groups}
for t in catalog["tasks"] + catalog["supplemental_tasks"]:
    check((out / t["file"]).exists(), f"Missing card file: {t['id']}")
    card = (out / t["file"]).read_text(encoding="utf-8-sig")
    check(f'id="{t["anchor"]}"' in card, f"Missing anchor: {t['id']}")
    check(t["status"] == "pending", f"Unverified WBS task marked complete: {t['id']}")
    deps = re.findall(r"G\d{2}", t["dependencies"])
    if t.get("depends_on_task"):
        deps.append(t["depends_on_task"])
    graph[t["id"]] = deps
for t in catalog["priority_tasks"]:
    graph[t["id"]] = re.findall(r"R\d{2}", t["depends_on"])
seen, visiting = set(), set()
def visit(node):
    if node in visiting:
        errors.append("Dependency cycle at " + node)
        return
    if node in seen:
        return
    visiting.add(node)
    for dep in graph.get(node, []):
        check(dep in graph, "Unknown dependency " + dep)
        visit(dep)
    visiting.remove(node)
    seen.add(node)
for key in graph:
    visit(key)
link_count = 0
for md in [root / "task_plan.md", root / "findings.md"] + list(out.glob("*.md")):
    text = md.read_text(encoding="utf-8-sig")
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if link.startswith(("http:", "https:", "app:")):
            continue
        path, _, anchor = link.partition("#")
        path = re.sub(r":\d+$", "", path)
        target = Path(path)
        if not target.is_absolute():
            target = md.parent / target
        check(target.exists(), f"Broken link in {md.name}: {link}")
        if anchor and target.exists():
            content = target.read_text(encoding="utf-8-sig")
            check(f'id="{anchor}"' in content, f"Missing target anchor: {link}")
        link_count += 1
report = {
    "status": "pass" if not errors else "fail",
    "source_checkboxes": len(expected),
    "mapped_checkboxes": len(actual),
    "high_level_requirements": len(catalog["requirements"]),
    "wbs_implementation_tasks": sum(t["group"] < 29 for t in catalog["tasks"]),
    "supplemental_tasks": len(catalog["supplemental_tasks"]),
    "acceptance_criteria": sum(t["group"] == 29 for t in catalog["tasks"]),
    "priority_slice_tasks": len(catalog["priority_tasks"]),
    "dependency_nodes": len(graph),
    "links_checked": link_count,
    "source_unchanged": hashlib.sha256(source.read_bytes()).hexdigest() == catalog["source_sha256"],
    "product_tests_run_this_turn": False,
    "errors": errors,
}
(out / "plan_validation.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))

