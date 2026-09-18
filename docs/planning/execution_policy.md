# Quy tắc thực thi và quyết định cần theo dõi

## Phạm vi phiên lập lại kế hoạch

Người dùng yêu cầu chia lại bằng planning-with-files thành task nhỏ chi tiết. Phiên này chỉ lập kế hoạch, không triển khai thêm code sản phẩm. Phạm vi dài hạn vẫn là toàn roadmap. Ảnh là ví dụ sử dụng skill; không suy ra yêu cầu cài find-skills, khởi động lại Codex, tạo remote hay deploy.

## Trạng thái và bằng chứng

- pending: chưa bắt đầu hoặc chưa có bằng chứng đủ.
- in_progress: đang xử lý một task cụ thể.
- complete: output + kiểm chứng + evidence đầy đủ.
- Blocker ghi thành trường riêng, không dùng complete cho "đã có file".
- Mục optional không làm phải ghi quyết định phạm vi; không đổi thành complete giả.
- Cấu hình dự kiến, dependency cài được và code tồn tại là ba loại bằng chứng khác nhau.
- Ưu tiên một task đang làm; khi task chờ dữ liệu/tài khoản, ghi lại và chuyển task độc lập. Không yêu cầu subagent.

## Thứ tự và phụ thuộc

Bắt đầu R01–R14. Sau đó theo gate nhóm:
G00 → G01 → G02 → G03 → G04 → G06 → G05 → G07 → G08 → G10 → G12 → G13 → G09 → G14 → G11 → G15 → G18 → G16 → G17 → G20 → G19 → G21 → G22 → G23 → G24 → G25 → G26 → G27 → G28 → G29.

Đây là thứ tự bảo thủ để làm từng việc, không phải khẳng định mọi nhóm phụ thuộc trực tiếp nhóm đứng trước. Phụ thuộc thật ghi trong đầu mỗi WBS file. Test và tài liệu viết cùng task; G23/G27 là tổng hợp và kiểm chứng liên thông cuối, không phải hoãn kiểm thử đến cuối.

Các task "save scaler" chỉ cần dữ liệu train đã split; dataset windows ban đầu dùng raw features, nên G06 có thể chốt trước G05. Kiến trúc nâng cao dùng training/evaluation harness của baseline; không bắt baseline đợi Transformer.

## Cổng nghiệm thu

- M0 — Môi trường: R01–R04; baseline test được ghi, test không đè checkpoint.
- M1 — Dữ liệu: G01–G06 và S01/S03/S08; provenance, units, UTC, leakage và split có kiểm chứng.
- M2 — Model: G07–G15 và S02/S04/S05/S06; model/baseline được so cùng dữ liệu, calibration riêng, bundle reload được.
- M3 — Backend: G16–G20 và S09/S15/S24; dùng artifact thật fixture, migration PostGIS, worker/cache idempotent.
- M4 — Sản phẩm: G21/G22 và S10–S14; map/mobile/VI-EN, subscription ownership, alert draft/fake delivery có test.
- M5 — Vận hành: G23–G26 và S16–S20/S23; build/test/load, staging, rollback, monitoring, restore có evidence.
- M6 — Bàn giao: G27/G28/G29 và S21/S22; tất cả tiêu chí bắt buộc có bằng chứng, external pending được nêu rõ.

## Quyết định kỹ thuật dự kiến

- Giữ src/typhoon_vn; map thư mục logic trong roadmap vào package đang có, không tạo bản sao ở src/ingestion.
- Python 3.11; pyproject làm nguồn dependency; lockfile/pin tái lập được xử lý trong G00.
- React + TypeScript + Leaflet ở viz/frontend là phương án frontend đề xuất. Chốt toolchain/build trong task setup, không khẳng định đã cài.
- PostgreSQL/PostGIS + Alembic cho vận hành; SQLite chỉ hỗ trợ test/demo local, không thay nghiệm thu PostGIS.
- MLflow cho experiments/registry; DVC cho version dữ liệu; kiểm chứng quyền nguồn trước tải thật.
- Direct multi-horizon là đường chính; rolling là thí nghiệm có contract thời gian rõ.
- Theo dõi môi trường bằng available_at/issue_time để không lấy ERA5 hoàn thiện sau sự kiện làm "feature realtime".
- Persistence/heuristic là baseline có nhãn rõ; class tên CLIPER hiện tại cần thẩm định phương pháp.
- Chỉ phát hành uncertainty như coverage khi có calibration evidence; bán kính minh họa không phải xác suất.
- Endpoint impact phải phân biệt khoảng cách, giao cone tâm bão và hazard gió/lũ/đổ bộ.

## Tách validation, benchmark và final test

Roadmap có yêu cầu promotion theo test cố định và cũng cấm dùng test để tune. Giải quyết bằng hợp đồng rõ:
1. Train để fit weights/scaler.
2. Validation hoặc CV để chọn architecture/hyperparameters.
3. Calibration riêng cho uncertainty.
4. Benchmark phát hành quản trị theo version để kiểm tra promotion, có ghi lịch sử số lần đánh giá.
5. Final held-out test dùng sau khi khóa lựa chọn; không quay lại tune trên chính tập đó. Nếu kết quả dẫn tới thay thiết kế, đánh giá tương lai phải có tập holdout mới/quy trình đánh giá được ghi.

Không tự đặt con số chất lượng khí tượng hoặc SLO production thiếu dữ liệu. G13/G23 ghi baseline, đề xuất ngưỡng định lượng rồi khóa trong cấu hình evaluation gate trước khi chạy đánh giá ứng viên.

## Các điểm cần làm rõ khi đến đúng task

- URL/quyền truy cập NCHMF, CMA, JTWC, ERA5; chỉ hỏi khi không xác minh được từ nguồn công khai/fixtures.
- Ranh giới hành chính có phiên bản/ngày hiệu lực và giấy phép; không tự coi dữ liệu cũ là hiện hành.
- Danh sách historical storms, dung lượng và ngân sách CPU/GPU.
- Git remote và hosting chưa có; không tạo develop/remote/push chỉ vì checklist trong tài liệu ghi như vậy.
- Phương án user/session/auth và public/private dashboard; không đưa API key quản trị vào browser.
- Người nhận, nội dung và credentials cho kênh cảnh báo. Test mặc định qua fake transport/draft; gửi tin thật cần chỉ dẫn rõ.
- Hosting, domain, chi phí và thời điểm phát hành thật; chuẩn bị config và test local trước khi cần các thông tin này.

Các mục này không chặn lập kế hoạch, fixture tests hay code cục bộ đã được ủy quyền.

## Sổ bằng chứng

Mỗi file docs/planning/evidence/<ID>.md ghi:
- ID, thời gian, input/source/dataset/model version.
- File thay đổi và mục đích.
- Lệnh hoặc thao tác, expected, actual, exit code.
- Tệp test report/screenshot/artifact nếu có.
- Lỗi còn lại, quyết định scope, task kế tiếp.

Không tạo hàng trăm evidence rỗng. Chỉ tạo khi có việc thực sự đã thực hiện. task_catalog.json là chỉ mục ban đầu; task card là trạng thái chuẩn. Khi cập nhật task, đồng bộ catalog hoặc tái tạo chỉ mục bằng công cụ chỉ đọc card; không chạy lại generator khởi tạo để ghi đè trạng thái.

