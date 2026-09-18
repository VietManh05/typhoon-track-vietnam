
from pathlib import Path
import json,re
root=Path.cwd()
out=root/"docs/planning"
catalog=json.loads((out/"task_catalog.json").read_text(encoding="utf-8"))
if catalog.get("supplemental_tasks"):
    raise SystemExit("Refuse to overwrite an existing supplemental plan.")
extra=json.loads((out/"tools/supplemental.json").read_text(encoding="utf-8-sig"))
doc=["# Task bổ sung từ yêu cầu tổng quan","",
"Các task S cụ thể hóa mục còn thiếu task độc lập hoặc cần scope rõ trong WBS. Không thay thế task T trùng thành phần: tái dùng output/test đã nghiệm thu. Optional phải có quyết định phạm vi, không tự coi hoàn tất.",""]
supp=[]
for identifier,title,deps,paths,steps,dod,keyword in extra:
    refs=[p for p in catalog["requirements"] if keyword.lower() in p["title"].lower()]
    links=", ".join("["+p["id"]+"](traceability.md)" for p in refs) or "Phân rã bổ sung từ phạm vi tổng quan của roadmap"
    doc += [f'<a id="{identifier.lower()}"></a>',f"## {identifier} — {title}","",
            "- **Trạng thái:** pending.",f"- **Phụ thuộc:** {deps}.",
            f"- **Nguồn:** {links}.",f"- **File/đầu ra:** {paths}.",
            f"- **Thực hiện:** {steps}",f"- **Kiểm thử/DoD:** {dod}",
            f"- **Bằng chứng:** evidence/{identifier}.md — chưa thực hiện.",""]
    supp.append({"id":identifier,"title":title,"dependencies":deps,"status":"pending",
                 "file":"supplemental_tasks.md","anchor":identifier.lower(),
                 "source_requirements":[p["id"] for p in refs]})
(out/"supplemental_tasks.md").write_text("\n".join(doc),encoding="utf-8")
catalog["supplemental_tasks"]=supp
# Explicit ordering inside each subsection: small work units, not all-at-once.
previous={}
for task in catalog["tasks"]:
    key=(task["group"],task["section"])
    predecessor=previous.get(key)
    task["depends_on_task"]=predecessor
    previous[key]=task["id"]
    path=out/task["file"]
    text=path.read_text(encoding="utf-8")
    start=text.index('## '+task["id"]+' —')
    end=text.find('\n## ',start+1)
    end=len(text) if end<0 else end
    card=text[start:end]
    order=(f'- **Task trước trong tiểu mục:** {predecessor}; kiểm tra output trước khi bắt đầu.\n'
           if predecessor else '- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.\n')
    card=card.replace('- **Đầu vào:**',order+'- **Đầu vào:**',1)
    text=text[:start]+card+text[end:]
    path.write_text(text,encoding="utf-8")
(out/"task_catalog.json").write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
p=out/"README.md"
s=p.read_text(encoding="utf-8").replace("**635 task WBS**,","**635 task WBS + 24 task bổ sung = 659 task thực thi**,")
p.write_text(s,encoding="utf-8")
with (out/"traceability.md").open("a",encoding="utf-8") as f:
    f.write("\n## Phân rã thêm yêu cầu tổng quan\n\n")
    for t in supp:
        f.write("- ["+t["id"]+"](supplemental_tasks.md#"+t["anchor"]+") — "+t["title"]+
                "; nguồn: "+(", ".join(t["source_requirements"]) or "phạm vi tổng quan")+"\n")
print("Supplemental tasks and per-task ordering recorded.")

