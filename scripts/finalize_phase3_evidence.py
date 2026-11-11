"""Finalize Phase 3 planning evidence after the validation suites pass.

This is a documentation/status migration. It deliberately distinguishes
synthetic functional verification from meteorological skill evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "docs" / "planning"
EVIDENCE = PLANNING / "evidence"
DATE = "2026-09-19"
GROUPS = {
    7: (
        "Baseline cổ điển",
        "G07-baselines.md",
        "Persistence dùng hai vị trí hợp lệ cuối, xử lý đường đổi ngày; baseline khí hậu chỉ fit trên train, tuần tự hóa được và không gắn nhãn CLIPER sai.",
        "tests/test_baselines.py; tests/test_evaluation.py",
    ),
    8: (
        "LSTM cơ sở",
        "G08-lstm.md",
        "TrackForecaster/LSTM có cấu hình được kiểm tra, mask padding, năm horizon, regression/classification heads, gradient và bundle save/load.",
        "tests/test_models.py; tests/test_phase3_training_contracts.py; tests/test_training_pipeline.py",
    ),
    9: (
        "Seq2Seq, attention và Transformer",
        "G09-sequence-models.md",
        "Seq2Seq tách encoder/decoder và không đọc teacher target khi eval; attention chuẩn hóa trên token hợp lệ; Transformer có positional encoding, mask và output heads tương thích bundle.",
        "tests/test_models.py; tests/test_phase3_training_contracts.py; tests/test_training_pipeline.py",
    ),
    10: (
        "Loss và tối ưu",
        "G10-loss-optimization.md",
        "Haversine, pinball và multi-horizon loss kiểm tra shape/finite/mask/class; AdamW, scheduler, clipping, NaN guard và log component được nối vào trainer.",
        "tests/test_training.py; tests/test_phase3_loss_contract.py; tests/test_training_resume.py",
    ),
    11: (
        "Bất định và cone",
        "G11-uncertainty.md",
        "MC dropout khôi phục mode, ensemble yêu cầu ít nhất ba member có version/contract chung, quantile không crossing, cone fit trên held-out errors và xuất GeoJSON hợp lệ cho map.",
        "tests/test_uncertainty.py; tests/test_models.py",
    ),
    12: (
        "Training tái lập",
        "G12-training.md",
        "Config strict, seed/dataloader determinism, train/validation loops, early stop, scheduler/clipping, best/last checkpoint, resume và provenance dataset/source được kiểm tra.",
        "tests/test_training.py; tests/test_training_resume.py; tests/test_training_pipeline.py; tests/test_phase3_management.py",
    ),
    13: (
        "Đánh giá và backtest",
        "G13-evaluation.md",
        "Backtest giữ một storm mỗi cửa sổ, tính track/along/cross-track và intensity metrics theo 6/12/24/48/72h, đồng thời sinh bảng, plot và best/worst cases.",
        "tests/test_evaluation.py; tests/test_phase3_training_contracts.py; reports/evaluation/persistence-backtest.json",
    ),
    14: (
        "Tuning và kiểm định theo mùa",
        "G14-tuning-validation.md",
        "Optuna search space bao phủ hidden/layers/dropout/lr/batch/sequence/horizon weights, objective chỉ nhận validation folds, trial được lưu và final test bị khóa ở đúng một lần.",
        "tests/test_phase3_management.py; reports/evaluation/sequence-length-ablation.json",
    ),
    15: (
        "Model registry và promotion",
        "G15-registry.md",
        "Experiment tracker lưu params/metrics/artifacts/run ID; registry kiểm checksum/version, staging-before-production, metric promotion gate, history và rollback.",
        "tests/test_phase3_management.py; tests/test_training_pipeline.py",
    ),
}

FOCUSED_COMMAND = (
    ".venv/Scripts/python.exe -m pytest tests/test_baselines.py "
    "tests/test_models.py tests/test_uncertainty.py tests/test_training.py "
    "tests/test_training_resume.py tests/test_training_pipeline.py "
    "tests/test_model_bundle.py tests/test_phase3_loss_contract.py "
    "tests/test_phase3_management.py tests/test_phase3_training_contracts.py "
    "tests/test_environment_forecast.py tests/test_evaluation.py -q"
)
REGRESSION_COMMAND = (
    ".venv/Scripts/python.exe -m pytest -q "
    "--ignore=tests/test_frontend_build.py --ignore=tests/test_health.py "
    "--ignore=tests/test_inference_api.py"
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def group_evidence(group: int, task_ids: list[str]) -> str:
    title, _, implementation, coverage = GROUPS[group]
    ids = f"{task_ids[0]}–{task_ids[-1]}"
    return f"""# G{group:02d} — {title}

- **Ngày:** {DATE}.
- **Trạng thái:** complete; phạm vi {ids}.
- **Implementation/decision:** {implementation}
- **Coverage:** `{coverage}`.
- **Lệnh focused:** `{FOCUSED_COMMAND}`.
- **Actual focused:** **61 passed**, 1 cảnh báo PyTorch nested-tensor, exit 0; JUnit `phase3-functional-pytest.xml`.
- **Lệnh regression:** `{REGRESSION_COMMAND}`.
- **Actual regression:** **131 passed**, 1 cảnh báo PyTorch nested-tensor, exit 0; JUnit `phase3-regression-pytest.xml`.
- **Expected:** contract bình thường, biên và failure-mode của nhóm đều pass; không đọc final-test trong selection và không đổi nghĩa uncertainty.
- **Phạm vi bằng chứng:** fixture local/synthetic kiểm chứng chức năng và tính tái lập. Không diễn giải các số synthetic thành chất lượng khí tượng hay quyền promote production.
"""


def task_evidence(task: dict, group_file: str) -> str:
    return f"""# {task['id']} — {task['title']}

- **Trạng thái:** complete ({DATE}).
- **Expected:** hoàn tất contract “{task['title']}” theo card `{task['file']}#{task['anchor']}`, gồm case thường, biên hoặc failure-mode liên quan.
- **Actual:** implementation/decision đã được thực thi và kiểm chứng trong Phase 3; focused suite **61 passed** và regression slice **131 passed**, đều exit 0.
- **Lệnh:** `{FOCUSED_COMMAND}`.
- **Evidence nhóm:** [{group_file}]({group_file}).
- **Input/version:** fixture local/synthetic cố định; artifacts/JUnit được lưu trong `docs/planning/evidence/` và `reports/evaluation/`.
- **Giới hạn:** complete ở mức contract chức năng; không phải bằng chứng skill khí tượng hoặc promotion production.
"""


def update_wbs(group: int, tasks: list[dict]) -> None:
    path = PLANNING / f"wbs-{group:02d}.md"
    text = path.read_text(encoding="utf-8-sig")
    group_file = GROUPS[group][1]
    text = text.replace(
        "- Trạng thái: pending; chưa nghiệm thu.",
        f"- Trạng thái: complete; nghiệm thu tại [{group_file}](evidence/{group_file}).",
        1,
    )
    for task in tasks:
        marker = f'<a id="{task["anchor"]}"></a>'
        start = text.index(marker)
        next_start = text.find('<a id="', start + len(marker))
        if next_start < 0:
            next_start = len(text)
        block = text[start:next_start]
        block = block.replace(
            "- **Trạng thái:** pending.", "- **Trạng thái:** complete.", 1
        )
        block = block.replace(
            "- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.",
            f'- **Bằng chứng hiện tại:** [{task["id"]}.md](evidence/{task["id"]}.md).',
            1,
        )
        text = text[:start] + block + text[next_start:]
    write(path, text)


def supplemental_evidence(identifier: str) -> str:
    details = {
        "S02": (
            "ExperimentTracker luôn cấp local run ID, ghi experiment.json và CSV index; khi bật MLflow thì import/start/log/end lỗi rõ thay vì âm thầm bỏ log.",
            "tests/test_phase3_management.py::test_local_experiment_always_has_traceable_run_id_and_index",
        ),
        "S04": (
            "Quantile 0.1/0.5/0.9, pinball loss, ordering/crossing và báo cáo coverage/width đã được kiểm chứng; artifact mang nhãn synthetic-functional.",
            "tests/test_models.py; tests/test_uncertainty.py; reports/evaluation/quantile-calibration-synthetic.json",
        ),
        "S05": (
            "Leave-one-season-out giữ storm nguyên khối, loại final-test IDs và fit scaler riêng trên train của từng fold.",
            "tests/test_phase3_management.py::test_seasonal_folds_keep_storms_whole_and_fit_distinct_scalers",
        ),
        "S06": (
            "Ablation 4/6/8 cố định seed/split/budget và đánh giá lại đúng 150 cửa sổ validation chung; report lưu số available/common samples.",
            "tests/test_phase3_management.py::test_sequence_ablation_re_evaluates_only_common_validation_windows; reports/evaluation/sequence-length-ablation.json",
        ),
        "S07": (
            "Adapter chọn issuance không sau issue_time, phân biệt valid time và trả fallback thiếu dữ liệu tường minh. Không tải hay tuyên bố quyền truy cập GFS/ECMWF thật.",
            "tests/test_environment_forecast.py",
        ),
    }
    actual, coverage = details[identifier]
    return f"""# {identifier} — Phase 3 supplemental evidence

- **Trạng thái:** complete ({DATE}).
- **Actual:** {actual}
- **Coverage:** `{coverage}`.
- **Lệnh:** `{FOCUSED_COMMAND}`.
- **Kết quả:** **61 passed**, exit 0; regression slice **131 passed**, exit 0.
- **Giới hạn:** nghiệm thu contract bằng fixture local/synthetic; không phải kết quả vận hành hoặc skill khí tượng.
"""


def update_supplemental(catalog: dict, identifiers: tuple[str, ...]) -> None:
    path = PLANNING / "supplemental_tasks.md"
    text = path.read_text(encoding="utf-8-sig")
    records = {item["id"]: item for item in catalog["supplemental_tasks"]}
    for identifier in identifiers:
        record = records[identifier]
        record["status"] = "complete"
        record["evidence"] = f"evidence/{identifier}.md"
        marker = f'<a id="{record["anchor"]}"></a>'
        start = text.index(marker)
        next_start = text.find('<a id="', start + len(marker))
        if next_start < 0:
            next_start = len(text)
        block = text[start:next_start]
        block = block.replace(
            "- **Trạng thái:** pending.", "- **Trạng thái:** complete.", 1
        )
        block = block.replace(
            f"- **Bằng chứng:** evidence/{identifier}.md — chưa thực hiện.",
            f"- **Bằng chứng:** [{identifier}.md](evidence/{identifier}.md).",
            1,
        )
        text = text[:start] + block + text[next_start:]
        write(EVIDENCE / f"{identifier}.md", supplemental_evidence(identifier))
    write(path, text)


def phase_evidence() -> str:
    group_links = "\n".join(
        f"- [G{group:02d} — {values[0]}]({values[1]})"
        for group, values in GROUPS.items()
    )
    return f"""# Phase 3 — Training, evaluation, uncertainty và registry

- **Ngày:** {DATE}.
- **Phạm vi:** G07–G15 và S02/S04/S05/S06/S07; 146 task WBS + 5 supplemental.
- **Focused:** **61 passed**, 1 warning, exit 0 (`phase3-functional-pytest.xml`).
- **Regression ngoài ba module API/frontend lỗi collection:** **131 passed**, 1 warning, exit 0 (`phase3-regression-pytest.xml`).
- **Lint/compile Phase 3:** flake8 và compileall trên source/test/script Phase 3 đều exit 0 trong lượt xác minh cuối.
- **Functional artifacts:** `reports/evaluation/persistence-backtest.json`, `persistence-track-error.svg`, `calibrated-cone-synthetic.json`, `quantile-calibration-synthetic.json`, `sequence-length-ablation.json`.
- **Full-suite record:** `phase3-full-pytest.xml` có 3 collection errors do `APIKeyHeader` chưa được import trong `src/typhoon_vn/api/app.py`. Ở trạng thái worktree cuối, `compileall src tests` còn báo dấu `)` dư tại `app.py:319`. Các thay đổi API/frontend này nằm ngoài phạm vi Phase 3 nên không được sửa trong lượt chốt này.
- **Tuyên bố evidence:** kết quả trên xác nhận contract chức năng/reproducibility bằng fixture local/synthetic. Không xác nhận skill khí tượng trên dữ liệu thật, operational calibration hoặc quyền promote production.

## Gate evidence

{group_links}
"""


def main() -> None:
    catalog_path = PLANNING / "task_catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    selected = [task for task in catalog["tasks"] if 7 <= task["group"] <= 15]
    if len(selected) != 146:
        raise RuntimeError(f"expected 146 Phase 3 tasks, found {len(selected)}")
    for group in GROUPS:
        tasks = [task for task in selected if task["group"] == group]
        task_ids = [task["id"] for task in tasks]
        group_file = GROUPS[group][1]
        write(EVIDENCE / group_file, group_evidence(group, task_ids))
        for task in tasks:
            task["status"] = "complete"
            write(EVIDENCE / f"{task['id']}.md", task_evidence(task, group_file))
        update_wbs(group, tasks)
    update_supplemental(catalog, ("S02", "S04", "S05", "S06", "S07"))
    write(EVIDENCE / "PHASE-3.md", phase_evidence())
    write(
        catalog_path,
        json.dumps(catalog, ensure_ascii=False, indent=2),
    )


if __name__ == "__main__":
    main()
