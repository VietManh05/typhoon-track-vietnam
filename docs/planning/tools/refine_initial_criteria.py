from pathlib import Path
import ast,json,re
out=Path("docs/planning")
p=out/"tools/build_initial_plan.py"
s=p.read_text(encoding="utf-8-sig")
s=s.replace("if any(term in t for term in terms):",
            'if any(re.search(r"(?<!\\w)"+re.escape(term)+r"(?!\\w)",t) for term in terms):')
p.write_text(s,encoding="utf-8")
tree=ast.parse(s)
function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="checks")
namespace={"re":re}
exec(compile(ast.Module(body=[function],type_ignores=[]),str(p),"exec"),namespace)
catalog=json.loads((out/"task_catalog.json").read_text(encoding="utf-8"))
by_file={}
for t in catalog["tasks"]:
    by_file.setdefault(t["file"],[]).append(t)
for filename,tasks in by_file.items():
    path=out/filename
    text=path.read_text(encoding="utf-8")
    for t in tasks:
        start=text.index("## "+t["id"]+" —")
        end=text.find("\n## ",start+1)
        if end<0: end=len(text)
        card=text[start:end]
        criterion=namespace["checks"](t["title"],t["group"])
        if "window" in t["title"].lower():
            criterion="Cửa sổ chỉ chứa một storm, input_len đúng; fixture ngắn hơn window không tạo sample; timestamps không đảo hoặc trùng."
        card=re.sub(r"(?m)^- \*\*Kiểm thử riêng:\*\* .*",
                    lambda m:"- **Kiểm thử riêng:** "+criterion,card)
        text=text[:start]+card+text[end:]
    path.write_text(text,encoding="utf-8")
# Prevent accidentally re-running the one-shot supplemental initializer.
p=out/"tools/finalize_initial_plan.py"
s=p.read_text(encoding="utf-8-sig")
s=s.replace('extra=json.loads',
            'if catalog.get("supplemental_tasks"):\n    raise SystemExit("Refuse to overwrite an existing supplemental plan.")\nextra=json.loads',1)
p.write_text(s,encoding="utf-8")
print("Refined operation-specific criteria; guarded initializers.")

