
from pathlib import Path
import re, json, hashlib, shutil
from collections import defaultdict
groups=json.loads((Path(__file__).parent/"groups.json").read_text(encoding="utf-8-sig"))
subspecs=json.loads((Path(__file__).parent/"subsections.json").read_text(encoding="utf-8-sig"))
first_tasks=json.loads((Path(__file__).parent/"priority.json").read_text(encoding="utf-8-sig"))
root=Path.cwd()
out=root/"docs/planning"
out.mkdir(parents=True,exist_ok=True)
if (out/"task_catalog.json").exists():
    raise SystemExit("Refuse to regenerate an existing plan; preserve task statuses.")
history=out/"history/2026-09-18-before-replan"
history.mkdir(parents=True,exist_ok=True)
for name in ("task_plan.md","findings.md","progress.md"):
    target=history/name
    if (root/name).exists() and not target.exists():
        shutil.copy2(root/name,target)
source=root/"ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md"
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
lines=source.read_text(encoding="utf-8").splitlines()
records=[]
group=None
section=""
detailed=False
high_section=""
seq=defaultdict(int)
parents=[]
for line_no,line in enumerate(lines,1):
    if line.startswith("# WBS CHI"):
        detailed=True
    if not detailed:
        if line.startswith("#"):
            high_section=line.lstrip("# ").strip()
        if re.match(r"^- \[[ xX]\]",line):
            parents.append({"line":line_no,"title":line[6:].strip(),"section":high_section})
        continue
    match=re.match(r"^#{1,3} (\d+)\.\s+(.+)",line)
    if match:
        group=int(match.group(1))
        section=match.group(1)+". "+match.group(2)
    elif line.startswith("#"):
        section=line.lstrip("# ").strip()
    if re.match(r"^- \[[ xX]\]",line) and group is not None and group<=29:
        seq[group]+=1
        identifier=("A" if group==29 else "T")+f"{group:02d}-{seq[group]:03d}"
        records.append({"id":identifier,"group":group,"section":section,
                        "line":line_no,"title":line[6:].strip(),"status":"pending"})

def source_link(n):
    return "["+str(n)+"]("+source.as_posix()+":"+str(n)+")"

def checks(title,g):
    t=title.lower()
    rules=[
    (("checksum","hash"),"Cùng bytes cho cùng SHA-256; đổi một byte làm đổi digest; digest gắn với input version."),
    (("timezone","utc","timestamp","thời điểm","thời gian"),"UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt."),
    (("retry","timeout"),"Fake transport lỗi rồi thành công; số lần thử/timeout theo cấu hình; hết retry có trạng thái thất bại và log."),
    (("missing","thiếu","fallback","nội suy","interpolation"),"Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0."),
    (("split","train ids","validation ids","test ids","overlap","leakage"),"Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu."),
    (("scaler","inverse"),"Fit train-only; val/test cực trị không đổi stats; save/load giữ order/fill; finite round-trip <=1e-6."),
    (("latitude","longitude","lat/lon","tọa độ"),"Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ."),
    (("haversine","distance","khoảng cách"),"Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất."),
    (("bearing","direction"),"Hướng bắc/đông/tây đúng; 359→1 là đổi hướng nhỏ; điểm trùng có quy tắc công bố."),
    (("wind","pressure","unit","đơn vị","shear"),"Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa."),
    (("6h","12h","24h","48h","72h","horizon","target"),"Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay."),
    (("padding","mask","sequence","shape","tensor","batch-size"),"Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary."),
    (("checkpoint","resume","save/load"),"Reload đủ state; resume so với chạy liên tục; epoch/history/LR nhất quán; checkpoint mới không đè artifact khác."),
    (("nan","loss","gradient"),"Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả."),
    (("seed","deterministic"),"Lưu seed Python/NumPy/Torch/backend; cùng môi trường CPU/seed tái lập; khác seed thành run khác."),
    (("cache","redis","ttl","invalidation"),"Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision."),
    (("migration","alembic","foreign","constraint","index"),"DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật."),
    (("throttle","spam","send","channel"),"Fake transport không gửi trùng event qua restart/redelivery; cooldown đúng biên; không gửi tin thật trong test."),
    (("source","provenance","metadata","nguồn"),"Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức."),
    (("cone","polygon","geojson"),"GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa."),
    (("api key","rate limit","error handler"),"Test thiếu/sai/đúng key, vượt hạn mức; status/body đúng; log không chứa secret; UI không chứa admin key."),
    (("/forecast","/typhoons","/health","/version"),"TestClient kiểm tra valid/invalid input, status/schema/provenance và lỗi service; response không NaN."),
    (("responsive","mobile","tablet","accessibility"),"Thao tác ở 360×800,768×1024,1440×900; focus/keyboard rõ; không mất legend/disclaimer hoặc cuộn ngang."),
    (("mlflow","log","metric","evaluation","evaluate","backtest","f1","accuracy","rmse","median","mean"),"Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune."),
    (("download","tải","fetch"),"Mock bytes xác định và HTTP failure; checksum/raw giữ nguyên; lần tải thật phải có nguồn hợp lệ và evidence riêng."),
    (("docker","image","compose","build"),"Build/config exit 0; smoke service; secrets/raw/checkpoints ngoài build context trừ artifact được chọn."),
    (("test","kiểm tra","validate","validation"),"Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại."),
    (("readme","guide","documentation","runbook","disclaimer","architecture"),"Nội dung khớp implementation đã kiểm chứng; ví dụ chạy được; link đúng; phân biệt demo/thực nghiệm/vận hành.")]
    for terms,value in rules:
        if any(re.search(r"(?<!\w)"+re.escape(term)+r"(?!\w)",t) for term in terms):
            return value
    if g==0:
        return "Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng."
    if g==21:
        return "UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console."
    if g==28:
        return "Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate."
    if g==29:
        return "Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại."
    return "Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual."

by_group=defaultdict(list)
for r in records:
    by_group[r["group"]].append(r)
index=["# Kế hoạch chi tiết Typhoon VN","",
       "Ngày lập lại: 2026-09-18. Phạm vi: toàn roadmap; phiên hiện tại chỉ lập lại kế hoạch.",
       "Ảnh đính kèm là ngữ cảnh giải thích skill, không phải yêu cầu cài thêm skill hoặc khởi động lại ứng dụng.",
       "", "## Cách thực hiện từng task","",
       "1. Đọc task_plan.md → next_tasks.md → đúng task card.",
       "2. Kiểm tra dependency và code có sẵn; kiểm chứng/sửa phần thiếu, không viết lại mặc định.",
       "3. Một task in_progress tại một thời điểm; cập nhật Next Step.",
       "4. Lưu command, exit code, expected/actual và evidence; chỉ đánh complete khi đạt DoD.",
       "5. Thiếu dữ liệu/tài khoản thì giữ pending, ghi blocker và làm task độc lập. Không cần xin lại quyền cho sửa chữa đã được ủy quyền.",
       "6. Cập nhật findings/progress/task_plan sau mỗi task; không có bằng chứng thì chưa hoàn thành.",
       "", "## File điều phối","",
       "- [14 việc làm ngay](next_tasks.md)",
       "- [Quyết định và cổng nghiệm thu](execution_policy.md)",
       "- [Đối chiếu toàn bộ checkbox](traceability.md)",
       "- [Bổ sung yêu cầu chỉ có ở phần tổng quan](supplemental_tasks.md)",
       "- [Nghiệm thu toàn dự án](acceptance.md)","", "## WBS",""]
for g,title,paths,deps,inputs,dod,state in groups:
    entries=by_group[g]
    filename="acceptance.md" if g==29 else f"wbs-{g:02d}.md"
    index.append(f"- **G{g:02d} — {title}**: [{len(entries)} mục]({filename}); phụ thuộc: {deps}.")
    body=[f"# G{g:02d} — {title}","",
          "- Trạng thái: pending; chưa nghiệm thu.",
          f"- Hiện trạng: {state}.", f"- Đầu vào: {inputs}.",
          f"- Gate phụ thuộc: {deps}.",f"- Vùng file dự kiến: {paths}.",
          "- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.",
          "- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.",
          f"- DoD nhóm: {dod}.","",f'<a id="gate-g{g:02d}"></a>',f"## Gate G{g:02d}","",
          "Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.",""]
    for r in entries:
        title=r["title"]
        section=r["section"]
        prefix=re.match(r"(\d+\.\d+)",section)
        scenario=subspecs.get(prefix.group(1) if prefix else "",dod+".")
        evidence=f"evidence/{r['id']}.md"
        kind="kiểm chứng rồi bổ sung phần thiếu"
        if g==29:
            kind="nghiệm thu, không viết code trùng"
        elif g==28:
            kind="demo bằng chứng"
        elif g==27:
            kind="tài liệu dựa trên kết quả đã chạy"
        elif any(x in title.lower() for x in ("download toàn bộ","production deployment","deploy staging","send channel")):
            kind="chuẩn bị/test cục bộ trước; chạy thật cần nguồn, credentials và phạm vi vận hành phù hợp"
        r.update(file=filename,anchor=r["id"].lower(),kind=kind,dependencies=deps,evidence=evidence)
        body += [f'<a id="{r["anchor"]}"></a>',f'## {r["id"]} — {title}',"",
                 "- **Trạng thái:** pending.",
                 f'- **Nguồn:** {section}; dòng {source_link(r["line"])}.',
                 f"- **Loại:** {kind}.",
                 f"- **Phụ thuộc:** {deps}; contract/fixture của tiểu mục {section}.",
                 f"- **Đầu vào:** {inputs}; yêu cầu riêng: {title}",
                 f"- **File/đầu ra:** thay đổi nhỏ trong {paths}; evidence tại {evidence}.",
                 "- **Bước thực hiện:**",
                 f"  1. Định vị phần hiện có liên quan “{title}”; ghi phần đạt/chưa đạt và ví dụ input/output.",
                 f"  2. Hoàn thiện đúng mục này; giữ contract G{g:02d}, không mở rộng module khác ngoài phụ thuộc bắt buộc.",
                 "  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.",
                 f"- **Kiểm thử riêng:** {checks(title,g)}",
                 f"- **Kịch bản tiểu mục:** {scenario}",
                 "- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.",
                 "- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.",""]
    (out/filename).write_text("\n".join(body),encoding="utf-8")
task_count=sum(r["group"]<29 for r in records)
index.insert(4,f"**{task_count} task WBS**, **{len(by_group[29])} tiêu chí nghiệm thu**, kèm **14 task ưu tiên** là lát cắt thực thi của backlog, không cộng trùng phạm vi.")
(out/"README.md").write_text("\n".join(index)+"\n",encoding="utf-8")
nextdoc=["# Việc làm ngay — xử lý tuần tự","",
"Đây là lát cắt đầu tiên của WBS. Phiên lập kế hoạch chưa thực hiện R01–R14. Mục tiêu: baseline đáng tin và train→bundle→API trước frontend.",
"Nếu task vượt một phiên làm việc, tách ID .1/.2 với output riêng. Không giả định thời lượng train/tải dữ liệu khi chưa đo.",""]
for identifier,title,deps,inputs,output,steps,dod in first_tasks:
    nextdoc += [f"## {identifier} — {title}","",
                "- **Trạng thái:** pending.",f"- **Phụ thuộc:** {deps}.",
                f"- **Đầu vào/lệnh dự kiến:** {inputs}.",f"- **Đầu ra:** {output}.",
                f"- **Thao tác:** {steps}",f"- **Nghiệm thu:** {dod}",
                "- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.",
                "- **Bằng chứng:** chưa có; điền sau khi chạy.",""]
nextdoc += ["## Mapping vào WBS","",
"R01–R04 → G00/G23; R05 → G01/G03/G17; R06–R08 → G04/G06; R09 → G05; R10 → G12; R11 → G15/G16; R12 → G00/G12/G16; R13 → G16/G17; R14 → G18/G19/G20/G22.",
"","## Nhật ký mỗi task","",
"- Task ID và trạng thái pending → in_progress → complete.",
"- File/hành vi thay đổi.",
"- Command, input, expected, actual, exit code.",
"- Blocker còn lại và task kế tiếp duy nhất.",""]
(out/"next_tasks.md").write_text("\n".join(nextdoc),encoding="utf-8")
mapping={"2":[0],"3":[1,2],"4":[3,4,5],"5":[6,7,8,9,10,11],"6":[12,13,14,15],
         "7":[16,17,18,19,20],"8":[21],"9":[22],"10":[23],"11":[24,25,26],
         "12":[27,28],"14":[1,6,11,23,26]}
trace=["# Đối chiếu nguồn và kế hoạch","",
f"- SHA-256 tài liệu nguồn: {source_hash}.",
"- Mỗi checkbox nguồn xuất hiện đúng một lần trong chỉ mục.",
"- Tổng quan trỏ tới nhóm thực hiện; WBS trỏ tới task; DoD trỏ tới tiêu chí.",
"- Coverage của kế hoạch không phải tỷ lệ implementation hoàn thành.","","## Tổng quan",""]
for i,p in enumerate(parents,1):
    number=re.match(r"(\d+)",p["section"])
    targets=mapping.get(number.group(1) if number else "",[0])
    p.update(id=f"REQ-{i:03d}",groups=targets)
    links=", ".join(f"[G{g:02d}](wbs-{g:02d}.md#gate-g{g:02d})" for g in targets)
    trace.append(f'- {p["id"]} · dòng {source_link(p["line"])} · {p["title"]} → {links}.')
trace += ["","## WBS và DoD",""]
for r in records:
    trace.append(f'- Dòng {source_link(r["line"])} · [{r["id"]}]({r["file"]}#{r["anchor"]}) · {r["title"]}')
(out/"traceability.md").write_text("\n".join(trace)+"\n",encoding="utf-8")
catalog={"schema_version":1,"source_file":source.name,"source_sha256":source_hash,
         "scope":"replanning only; implementation pending verification",
         "source_checkboxes":len(parents)+len(records),"requirements":parents,"tasks":records,
         "priority_tasks":[{"id":t[0],"status":"pending","depends_on":t[2]} for t in first_tasks]}
(out/"task_catalog.json").write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"source_checkboxes":len(parents)+len(records),"requirements":len(parents),
                  "tasks":task_count,"acceptance":len(by_group[29]),"priority":len(first_tasks)}))

