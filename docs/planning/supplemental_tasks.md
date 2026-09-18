# Task bổ sung từ yêu cầu tổng quan

Các task S cụ thể hóa mục còn thiếu task độc lập hoặc cần scope rõ trong WBS. Không thay thế task T trùng thành phần: tái dùng output/test đã nghiệm thu. Optional phải có quyết định phạm vi, không tự coi hoàn tất.

<a id="s01"></a>
## S01 — Version hóa dữ liệu bằng DVC

- **Trạng thái:** pending.
- **Phụ thuộc:** G00, G03.
- **Nguồn:** [REQ-012](traceability.md).
- **File/đầu ra:** pyproject.toml; .dvc/; dvc.yaml; docs/data-versioning.md.
- **Thực hiện:** Chọn dataset clean nhỏ; track checksum và pipeline dependency; cấu hình remote qua env; không đẩy dữ liệu thật trong task cài đặt.
- **Kiểm thử/DoD:** Thay input đổi hash/output; dvc repro với fixture tái tạo output; remote cần quyền và storage riêng.
- **Bằng chứng:** evidence/S01.md — chưa thực hiện.

<a id="s02"></a>
## S02 — Lưu sổ thí nghiệm và MLflow run ID

- **Trạng thái:** pending.
- **Phụ thuộc:** G12.
- **Nguồn:** [REQ-014](traceability.md).
- **File/đầu ra:** docs/experiment-log-template.md; training/pipeline.py.
- **Thực hiện:** Mỗi run ghi config, git/source hash, dataset/split/scaler version, metrics và artifact URI; sinh JSON/CSV index.
- **Kiểm thử/DoD:** Một run smoke có ID truy ngược artifact; log lỗi MLflow không âm thầm mất kết quả training.
- **Bằng chứng:** evidence/S02.md — chưa thực hiện.

<a id="s03"></a>
## S03 — Feature store có version và schema drift

- **Trạng thái:** pending.
- **Phụ thuộc:** G04, G05.
- **Nguồn:** [REQ-050](traceability.md).
- **File/đầu ra:** features/store.py; tests/test_feature_store.py.
- **Thực hiện:** Ghi manifest tên/order/dtype/units/version; fingerprint schema; test cột thêm/thiếu/đổi kiểu/thứ tự.
- **Kiểm thử/DoD:** Store round-trip giữ schema; incompatible schema bị từ chối trước train/serve.
- **Bằng chứng:** evidence/S03.md — chưa thực hiện.

<a id="s04"></a>
## S04 — Quantile regression 10/50/90%

- **Trạng thái:** pending.
- **Phụ thuộc:** G09, G13.
- **Nguồn:** [REQ-064](traceability.md).
- **File/đầu ra:** models/uncertainty.py; training/losses.py; tests/test_quantiles.py.
- **Thực hiện:** Thêm output quantile và pinball loss; kiểm tra crossing; so coverage/width trên calibration; không hiểu quantile lat/lon là xác suất polygon.
- **Kiểm thử/DoD:** Synthetic distribution có test loss/ordering; báo cáo calibration độc lập; chỉ chọn nếu validation chứng minh hữu ích.
- **Bằng chứng:** evidence/S04.md — chưa thực hiện.

<a id="s05"></a>
## S05 — Leave-one-season-out validation

- **Trạng thái:** pending.
- **Phụ thuộc:** G06, G12.
- **Nguồn:** [REQ-082](traceability.md).
- **File/đầu ra:** training/cross_validation.py; tests/test_cross_validation.py.
- **Thực hiện:** Sinh folds theo mùa; storm qua năm thuộc một fold; fit scaler từng train fold; giữ final test riêng.
- **Kiểm thử/DoD:** Không giao storm/season theo policy; aggregate metrics từng fold, không tái sử dụng scaler fit toàn bộ.
- **Bằng chứng:** evidence/S05.md — chưa thực hiện.

<a id="s06"></a>
## S06 — Thí nghiệm độ dài chuỗi 4/6/8

- **Trạng thái:** pending.
- **Phụ thuộc:** G13, G14.
- **Nguồn:** [REQ-084](traceability.md).
- **File/đầu ra:** configs/ablation/; reports/evaluation/.
- **Thực hiện:** Cố định split/seed/budget; chạy ba configs; thống kê số sample khả dụng để so sánh công bằng.
- **Kiểm thử/DoD:** Báo cáo validation cùng horizon và mẫu chung; không chọn config theo final test.
- **Bằng chứng:** evidence/S06.md — chưa thực hiện.

<a id="s07"></a>
## S07 — Adapter forecast môi trường GFS/ECMWF tùy chọn

- **Trạng thái:** pending.
- **Phụ thuộc:** G01, G04.
- **Nguồn:** [REQ-028](traceability.md).
- **File/đầu ra:** ingestion/providers/environment.py; tests/test_environment_forecast.py.
- **Thực hiện:** Phân biệt forecast issuance/valid time và reanalysis; cache run/lead/grid; fallback khi field chưa phát hành.
- **Kiểm thử/DoD:** Point-in-time join không chọn run sau issue_time; ghi optional nếu chưa có nguồn/quyền truy cập.
- **Bằng chứng:** evidence/S07.md — chưa thực hiện.

<a id="s08"></a>
## S08 — Import và chuẩn hóa nhãn thiệt hại/đổ bộ

- **Trạng thái:** pending.
- **Phụ thuộc:** G01, G02.
- **Nguồn:** [REQ-023](traceability.md).
- **File/đầu ra:** ingestion/providers/vietnam.py; tests/test_impact_labels.py.
- **Thực hiện:** Parse nhãn PCTT tách khỏi target track; mapping tên/mã tỉnh theo ngày hiệu lực; giữ source/checksum.
- **Kiểm thử/DoD:** Không đưa nhãn hậu sự kiện thành input forecast; duplicate/conflict có evidence.
- **Bằng chứng:** evidence/S08.md — chưa thực hiện.

<a id="s09"></a>
## S09 — Cắt/giao cone với tỉnh và bờ biển

- **Trạng thái:** pending.
- **Phụ thuộc:** G02, G11, G18.
- **Nguồn:** [REQ-023](traceability.md), [REQ-109](traceability.md), [REQ-113](traceability.md).
- **File/đầu ra:** inference/impact.py; tests/test_impact_geometry.py.
- **Thực hiện:** Dùng geodesic/polygon và spatial query; tách proximity, probability vùng tâm và hazard thật; định nghĩa ETA hoặc trả không đủ dữ liệu.
- **Kiểm thử/DoD:** Fixture giao/không giao/chạm biên; endpoint không gọi tâm-cone là gió/lũ; UI nêu giới hạn.
- **Bằng chứng:** evidence/S09.md — chưa thực hiện.

<a id="s10"></a>
## S10 — Hiển thị so sánh dự báo chính thức

- **Trạng thái:** pending.
- **Phụ thuộc:** G01, G13, G21.
- **Nguồn:** [REQ-120](traceability.md).
- **File/đầu ra:** evaluation/official_comparison.py; viz/frontend/.
- **Thực hiện:** Import bản tin phát hành thực tế; ghép cùng issue_time, valid_time, storm; overlay hai nguồn có nhãn.
- **Kiểm thử/DoD:** Không so best-track tương lai với forecast như cùng loại; không có bản tin thì hiển thị unavailable.
- **Bằng chứng:** evidence/S10.md — chưa thực hiện.

<a id="s11"></a>
## S11 — Giao diện Việt/Anh

- **Trạng thái:** pending.
- **Phụ thuộc:** G21.
- **Nguồn:** [REQ-115](traceability.md).
- **File/đầu ra:** viz/frontend/src/i18n/; tests/frontend/.
- **Thực hiện:** Externalize labels, errors, disclaimer, units, datetime; VN là mặc định đề xuất; nhớ lựa chọn ngôn ngữ.
- **Kiểm thử/DoD:** Chuyển VI/EN cập nhật toàn UI, không chỉ tiêu đề; UTC/giờ VN có nhãn; dữ liệu null không thành 0.
- **Bằng chứng:** evidence/S11.md — chưa thực hiện.

<a id="s12"></a>
## S12 — Màu/chú giải cường độ có tài liệu nguồn

- **Trạng thái:** pending.
- **Phụ thuộc:** G21.
- **Nguồn:** [REQ-106](traceability.md).
- **File/đầu ra:** viz/frontend/src/theme/; docs/frontend.md.
- **Thực hiện:** Quy định palette có contrast và ký hiệu bổ trợ; chỉ gọi chuẩn NCHMF khi đã xác minh tài liệu chính thức.
- **Kiểm thử/DoD:** Người không phân biệt màu vẫn hiểu severity; legend luôn hiện và unknown có style riêng.
- **Bằng chứng:** evidence/S12.md — chưa thực hiện.

<a id="s13"></a>
## S13 — Kênh email/SMS/Telegram/Zalo qua adapter

- **Trạng thái:** pending.
- **Phụ thuộc:** G22.
- **Nguồn:** [REQ-116](traceability.md).
- **File/đầu ra:** alerts/channels/; tests/test_alert_channels.py.
- **Thực hiện:** Định nghĩa transport interface; fake adapter trước, mỗi provider là task con riêng; credentials env, retry/idempotency/dead-letter.
- **Kiểm thử/DoD:** Test adapter không gửi thật; gửi tới người thật chỉ khi có chỉ dẫn rõ về người nhận/nội dung và thông tin tài khoản.
- **Bằng chứng:** evidence/S13.md — chưa thực hiện.

<a id="s14"></a>
## S14 — Webhook tích hợp tùy chọn

- **Trạng thái:** pending.
- **Phụ thuộc:** G17, G22.
- **Nguồn:** [REQ-121](traceability.md).
- **File/đầu ra:** api/webhooks.py; tests/test_webhooks.py.
- **Thực hiện:** Thiết kế payload version, chữ ký, timestamp chống replay và delivery ID; mock receiver; chặn URL nội bộ nếu user-configurable.
- **Kiểm thử/DoD:** Signature sai/replay bị reject; retry không nhân bản side effect; không đăng ký/gửi bên ngoài trong task test.
- **Bằng chứng:** evidence/S14.md — chưa thực hiện.

<a id="s15"></a>
## S15 — Lịch ingestion theo mùa bão

- **Trạng thái:** pending.
- **Phụ thuộc:** G01, G19.
- **Nguồn:** [REQ-031](traceability.md).
- **File/đầu ra:** ingestion/schedule.py; infra/scheduler/.
- **Thực hiện:** Tách lịch cập nhật lịch sử và live; định nghĩa timezone, mùa 6–11 theo roadmap; backfill checkpoint và retry tránh trùng.
- **Kiểm thử/DoD:** Fake clock kiểm tra trong/ngoài mùa, qua năm, outage; task không tự tạo automation Codex.
- **Bằng chứng:** evidence/S15.md — chưa thực hiện.

<a id="s16"></a>
## S16 — Chính sách checkpoint retention

- **Trạng thái:** pending.
- **Phụ thuộc:** G12, G15.
- **Nguồn:** [REQ-074](traceability.md).
- **File/đầu ra:** training/checkpoint_retention.py; tests/test_retention.py.
- **Thực hiện:** Dry-run trước; giữ best/last/promoted/pinned; chỉ xóa file thuộc run manifest và trong root đã kiểm tra.
- **Kiểm thử/DoD:** Fixture chứng minh không xóa promoted hoặc file người dùng; đường dẫn escape bị reject.
- **Bằng chứng:** evidence/S16.md — chưa thực hiện.

<a id="s17"></a>
## S17 — Pipeline retrain định kỳ

- **Trạng thái:** pending.
- **Phụ thuộc:** G14, G15, G25.
- **Nguồn:** [REQ-137](traceability.md).
- **File/đầu ra:**  .github/workflows/retrain.yml; docs/retraining.md.
- **Thực hiện:** Config lịch/budget/seed/split/evaluation gate; run thủ công với fixture trước; chưa cấu hình lịch chạy thật nếu chưa có compute.
- **Kiểm thử/DoD:** Pipeline tạo staging candidate có provenance; không tự promotion chỉ vì training xong; final test không biến thành objective tune.
- **Bằng chứng:** evidence/S17.md — chưa thực hiện.

<a id="s18"></a>
## S18 — Autoscaling và ngân sách tải

- **Trạng thái:** pending.
- **Phụ thuộc:** G23, G24, G26.
- **Nguồn:** [REQ-140](traceability.md), [REQ-155](traceability.md).
- **File/đầu ra:** infra/deploy/; tests/load/; docs/capacity.md.
- **Thực hiện:** Đo p95/memory/CPU/queue với tải synthetic; chốt SLO và min/max replicas dựa kết quả; ghi chi phí theo hosting khi chọn.
- **Kiểm thử/DoD:** Có load report và trigger/hysteresis; không tuyên bố đáp ứng mùa bão khi chưa chạy hạ tầng thật.
- **Bằng chứng:** evidence/S18.md — chưa thực hiện.

<a id="s19"></a>
## S19 — Backup DB/model và phục hồi

- **Trạng thái:** pending.
- **Phụ thuộc:** G18, G15, G24.
- **Nguồn:** [REQ-143](traceability.md).
- **File/đầu ra:** scripts/backup/; tests/integration/test_restore.py; docs/runbook.md.
- **Thực hiện:** Backup metadata/model/scaler/schema; retention và integrity; khôi phục DB/model sang môi trường mới; chốt RPO/RTO sau đo.
- **Kiểm thử/DoD:** Restore drill truy vấn observation và tái tạo forecast; backup tồn tại nhưng chưa restore không đủ DoD.
- **Bằng chứng:** evidence/S19.md — chưa thực hiện.

<a id="s20"></a>
## S20 — Giám sát drift và sai số trễ

- **Trạng thái:** pending.
- **Phụ thuộc:** G13, G19, G26.
- **Nguồn:** [REQ-142](traceability.md).
- **File/đầu ra:** operations/monitoring.py; infra/monitoring/.
- **Thực hiện:** Lưu train reference distributions; tính missing/schema/input drift; join forecast với actual chỉ cho đánh giá hậu nghiệm.
- **Kiểm thử/DoD:** Drift spike fixture được phát hiện; không dùng observed future làm input; cảnh báo có sample size và model version.
- **Bằng chứng:** evidence/S20.md — chưa thực hiện.

<a id="s21"></a>
## S21 — Báo cáo cuối mùa

- **Trạng thái:** pending.
- **Phụ thuộc:** G13, G26, G27.
- **Nguồn:** [REQ-148](traceability.md).
- **File/đầu ra:** reports/post-season/; docs/model-card.md.
- **Thực hiện:** Tổng hợp error/coverage theo horizon, vùng, cường độ, nguồn; ghi case xấu, thiếu dữ liệu và model changes.
- **Kiểm thử/DoD:** Mọi số liệu truy về prediction run/dataset; không tuyên bố vượt nghiệp vụ nếu thiếu official comparison phù hợp.
- **Bằng chứng:** evidence/S21.md — chưa thực hiện.

<a id="s22"></a>
## S22 — Slide/video bàn giao

- **Trạng thái:** pending.
- **Phụ thuộc:** G28.
- **Nguồn:** [REQ-150](traceability.md).
- **File/đầu ra:** docs/acceptance/demo-script.md; reports/demo/.
- **Thực hiện:** Chuẩn bị kịch bản 6 demos, screenshots và recording nếu môi trường hỗ trợ; ghi demo vs real, version và lỗi đã biết.
- **Kiểm thử/DoD:** Người khác chạy theo kịch bản; video/slide mô tả đúng sản phẩm đã nghiệm thu.
- **Bằng chứng:** evidence/S22.md — chưa thực hiện.

<a id="s23"></a>
## S23 — Chọn hosting và diễn tập release/rollback

- **Trạng thái:** pending.
- **Phụ thuộc:** G24, G25.
- **Nguồn:** [REQ-139](traceability.md).
- **File/đầu ra:** docs/deployment.md; infra/deploy/.
- **Thực hiện:** Ghi yêu cầu availability, region, storage, secret/TLS; chọn provider sau khi có constraint thực; chuẩn bị staging config và rollback checklist.
- **Kiểm thử/DoD:** Staging smoke+rollback có evidence trước production; provisioning/trả phí cần tài khoản và phạm vi triển khai cụ thể.
- **Bằng chứng:** evidence/S23.md — chưa thực hiện.

<a id="s24"></a>
## S24 — Đóng gói CLI clean-data và kiểm tra provenance

- **Trạng thái:** pending.
- **Phụ thuộc:** G01, G03, G04, G05.
- **Nguồn:** [REQ-009](traceability.md).
- **File/đầu ra:** src/typhoon_vn/cli.py; scripts/run_phase2.py; tests/test_cli.py.
- **Thực hiện:** Thay placeholder bằng orchestration callable; input/output/config flags; validate path; giữ metadata qua merge/bridge/export.
- **Kiểm thử/DoD:** CLI fixture raw→clean→features có provenance; raw hash không đổi; config/path sai exit nonzero.
- **Bằng chứng:** evidence/S24.md — chưa thực hiện.
