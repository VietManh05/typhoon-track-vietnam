# Việc làm ngay — xử lý tuần tự

Đây là lát cắt đầu tiên của WBS. Phiên lập kế hoạch chưa thực hiện R01–R14. Mục tiêu: baseline đáng tin và train→bundle→API trước frontend.
Nếu task vượt một phiên làm việc, tách ID .1/.2 với output riêng. Không giả định thời lượng train/tải dữ liệu khi chưa đo.

## R01 — Kiểm kê trạng thái làm việc

- **Trạng thái:** complete.
- **Phụ thuộc:** Không.
- **Đầu vào/lệnh dự kiến:** git status --short; git log -1; git diff --stat; rg --files src tests.
- **Đầu ra:** docs/planning/evidence/R01-inventory.md.
- **Thao tác:** Phân biệt file cũ, file mới của phiên, module thiếu và dữ liệu phải giữ. Kiểm tra có commit nền chưa; không add/xóa hàng loạt.
- **Nghiệm thu:** Liệt kê đường dẫn thật; ghi rõ git diff rỗng không chứng minh không có thay đổi nếu toàn bộ file untracked.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R02 — Kiểm tra Python và extras

- **Trạng thái:** complete.
- **Phụ thuộc:** R01.
- **Đầu vào/lệnh dự kiến:** .venv/Scripts/python.exe --version; pip check; import numpy,pandas,torch,fastapi,sqlalchemy,redis.
- **Đầu ra:** docs/planning/evidence/R02-environment.md.
- **Thao tác:** Ghi phiên bản, exit code và dependency conflicts; kiểm tra API extras riêng với training extras.
- **Nghiệm thu:** Python 3.11; pip check/import smoke pass hoặc ghi lỗi cụ thể; không ghi pass khi chưa chạy.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R03 — Cô lập checkpoint khi chạy test

- **Trạng thái:** complete.
- **Phụ thuộc:** R02.
- **Đầu vào/lệnh dự kiến:** tests/test_training.py; Trainer.save_checkpoint.
- **Đầu ra:** tests/test_training.py và fixture tmp_path.
- **Thao tác:** Test trainer đang dùng checkpoint_dir mặc định; chuyển test sang tmp_path trước full pytest; giữ nguyên checkpoint có sẵn.
- **Nghiệm thu:** Test chỉ ghi tmp_path; hash checkpoint có sẵn không đổi.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R04 — Chạy baseline pytest

- **Trạng thái:** complete.
- **Phụ thuộc:** R03.
- **Đầu vào/lệnh dự kiến:** .venv/Scripts/python.exe -m pytest -q --junitxml=<evidence>.
- **Đầu ra:** docs/planning/evidence/R04-pytest.xml và R04-baseline.md.
- **Thao tác:** Chạy suite một lần sau cài dependencies; phân loại lỗi có sẵn/lỗi integration mới; không chạy training demo dài.
- **Nghiệm thu:** Ghi passed/failed/skipped/duration, command và exit code; mỗi lỗi có tên test và reproducer.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R05 — Chốt schema và thời gian

- **Trạng thái:** complete.
- **Phụ thuộc:** R04.
- **Đầu vào/lệnh dự kiến:** ingestion/models.py; features/schema.py; api/schemas.py.
- **Đầu ra:** docs/contracts/observations.md; tests/contracts/test_observations.py.
- **Thao tác:** Map latitude/longitude→lat/lon, native wind→m/s, UTC, source/checksum và issue/valid/downloaded times.
- **Nghiệm thu:** Một fixture qua ba lớp giữ tọa độ, đơn vị, UTC, provenance; reject naive datetime, NaN và unknown units.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R06 — Sửa target theo thời gian thực

- **Trạng thái:** complete.
- **Phụ thuộc:** R05.
- **Đầu vào/lệnh dự kiến:** datasets/typhoon_dataset.py; fixture có gap.
- **Đầu ra:** tests/test_dataset.py; dataset implementation.
- **Thao tác:** Thêm test issue 00 UTC, thiếu +12 nhưng có +18, duplicate time và target không đủ; sửa timestamp lookup hoặc policy reject interval.
- **Nghiệm thu:** Không lấy +18 thay +12; target đúng 6/12/24/48/72h; không vượt storm boundary.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R07 — Sửa split storm/năm

- **Trạng thái:** complete.
- **Phụ thuộc:** R06.
- **Đầu vào/lệnh dự kiến:** split_by_storm_or_year; storm qua 31/12→01/01.
- **Đầu ra:** tests/test_dataset.py; split manifest.
- **Thao tác:** Test test_ratio=0, val_ratio=0, tổng ratio>=1, tập nhỏ và storm qua năm. Lưu IDs/seed/hash.
- **Nghiệm thu:** Storm không giao tập; ratio=0 không ép lấy một storm; không mất hàng; errors rõ.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R08 — Chốt feature order

- **Trạng thái:** complete.
- **Phụ thuộc:** R07.
- **Đầu vào/lệnh dự kiến:** FeatureBuilder; _default_feature_cols; dataset _build.
- **Đầu ra:** docs/contracts/features.md; tests/test_feature_contract.py.
- **Thao tác:** Xử lý chọn default features trước derived features; dùng một feature path; giữ vocabulary/order cố định.
- **Nghiệm thu:** Training và serving cùng input cho cùng matrix; missing/extra/reordered columns được phát hiện.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R09 — Kiểm chứng scaler train-only

- **Trạng thái:** complete.
- **Phụ thuộc:** R08.
- **Đầu vào/lệnh dự kiến:** FeatureScaler; split manifest; fixtures held-out extrema.
- **Đầu ra:** tests/test_scaling_contract.py; scaler artifact schema.
- **Thao tác:** Thay val/test cực trị; test NaN/Inf/all-missing columns; save/load và round-trip.
- **Nghiệm thu:** Train stats không đổi; fill/order được lưu; finite round-trip sai số <=1e-6; inference không fit lại.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R10 — Sửa checkpoint/resume

- **Trạng thái:** complete.
- **Phụ thuộc:** R09.
- **Đầu vào/lệnh dự kiến:** Trainer; tiny deterministic CPU model/loader.
- **Đầu ra:** tests/test_training_resume.py; trainer.py.
- **Thao tác:** So 2 epochs liên tục với 1+resume; save sau history/scheduler; lưu best_epoch, patience, optimizer, scheduler và RNG; reject empty/nonfinite validation.
- **Nghiệm thu:** LR/history/epoch/early stop nhất quán; weights khớp trong dung sai công bố; không tạo best giả.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** [R10-checkpoint-resume.md](evidence/R10-checkpoint-resume.md); JUnit độc lập [R10-pytest.xml](evidence/R10-pytest.xml), 61 passed.

## R11 — Hoàn thiện bundle contract

- **Trạng thái:** complete.
- **Phụ thuộc:** R10.
- **Đầu vào/lệnh dự kiến:** Model constructor; scaler/schema/dataset hash.
- **Đầu ra:** docs/contracts/model-bundle.md; training/pipeline.py hoặc inference/artifacts.py.
- **Thao tác:** Chốt version/config/features/horizons/scaler/checksum/calibration metadata; tạo interface load_bundle/predict_bundle đang thiếu.
- **Nghiệm thu:** Load/reload có test; corrupted checksum/schema mismatch bị reject; không nhận artifact chưa tin cậy.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R12 — Nối CLI train và integration smoke

- **Trạng thái:** complete.
- **Phụ thuộc:** R11.
- **Đầu vào/lệnh dự kiến:** configs/phase3_lstm.yaml; CLI placeholder; synthetic fixture.
- **Đầu ra:** cli.py; tests/integration/test_training_bundle.py.
- **Thao tác:** Đọc/validate config, split storm, fit train scaler, train 1 epoch nhỏ, export/reload bundle, forecast 5 horizons trong tmp_path.
- **Nghiệm thu:** CLI chạy thật exit 0; config sai exit nonzero; output có provenance; demo không được gọi là metric bão thật.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R13 — Nghiệm thu inference/API nháp

- **Trạng thái:** complete.
- **Phụ thuộc:** R12.
- **Đầu vào/lệnh dự kiến:** inference/service.py; api/app.py; schemas.py; test DB.
- **Đầu ra:** tests/test_inference.py; tests/test_api.py.
- **Thao tác:** Test observations/storm ID, stale/future, missing artifact, trained/baseline, auth, 429 và load-once.
- **Nghiệm thu:** Forecast qua bundle fixture; status đúng; source/time/model/uncertainty/disclaimer đủ; không NaN hoặc freshness cache sai.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## R14 — Đối chiếu gap vận hành

- **Trạng thái:** complete.
- **Phụ thuộc:** R13.
- **Đầu vào/lệnh dự kiến:** Store create_all; Redis setex; worker JSON snapshot.
- **Đầu ra:** docs/planning/evidence/R14-operational-gaps.md.
- **Thao tác:** Map migration/PostGIS, Redis read/invalidation, live provider/scheduler, alert ownership vào G18/G19/G20/G22.
- **Nghiệm thu:** Mỗi gap có task ID/reproducer/DoD; không tuyên bố production-ready; tiếp tục backlog theo phụ thuộc.
- **Giới hạn:** log vấn đề khác vào backlog; không sửa lan phạm vi.
- **Bằng chứng:** chưa có; điền sau khi chạy.

## Mapping vào WBS

R01–R04 → G00/G23; R05 → G01/G03/G17; R06–R08 → G04/G06; R09 → G05; R10 → G12; R11 → G15/G16; R12 → G00/G12/G16; R13 → G16/G17; R14 → G18/G19/G20/G22.

## Nhật ký mỗi task

- Task ID và trạng thái pending → in_progress → complete.
- File/hành vi thay đổi.
- Command, input, expected, actual, exit code.
- Blocker còn lại và task kế tiếp duy nhất.
