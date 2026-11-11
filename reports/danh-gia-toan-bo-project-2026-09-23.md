# Đánh giá toàn bộ project Typhoon VN — 23/09/2026

> Đây là snapshot **trước sửa**. Xem [kết quả cải thiện](ket-qua-cai-thien-2026-09-23.md)
> và [hướng dẫn nâng cấp](../docs/review-upgrade-2026-09-23.md) cho trạng thái sau sửa.

## Kết luận

Project có cấu trúc khá rõ, nhiều kiểm thử hợp đồng dữ liệu, API và training, nhưng **chưa đủ điều kiện nghiệm thu toàn bộ luồng dự báo hoặc triển khai production**. Rà soát phát hiện **15 vấn đề: 7 P1 và 8 P2**. Đáng chú ý nhất là sai đơn vị tọa độ giữa training và inference, backtest không sử dụng scaler của training, lỗi khởi động với database cũ/wheel, và các luồng dashboard không tương thích backend production.

235 test backend và 15 test frontend đạt không phủ định những lỗi này: nhiều test kiểm tra shape, round-trip, fixture hoặc từng module, trong khi lỗi xuất hiện tại ranh giới giữa các module và hình thức triển khai.

Ba P1 của review trước đều được xác nhận lại bằng tái hiện trong phiên này: R03, R04, R05. Không sửa mã ứng dụng trong đợt review này.

## Phạm vi và cách kiểm chứng

- Đánh giá working tree hiện tại, gồm cả file chưa được Git theo dõi; không chỉ diff so với main. HEAD tham chiếu: `5baf229bfc059a54a496dd2582eedc60f708d618`. HEAD không đại diện đầy đủ working tree đang có nhiều thay đổi.
- Môi trường thực chạy: Windows/PowerShell, Python 3.11.9 trong `.venv`.
- Rà soát cấu trúc và các đường đi chính: ingestion, cleaning/features, datasets/scaler, training/checkpoint/bundle, evaluation/registry, inference/API/auth, Store/migrations/cache/worker, alerts, weather, frontend/Pages Functions, Docker/nginx/CI/monitoring và tài liệu kế hoạch.
- Chạy toàn bộ pytest, test frontend, type-check, build frontend ra thư mục riêng, lint/format checks, kiểm tra dependency Python, plan validator và build wheel.
- Viết [script tái hiện độc lập](review-20260923-reproduce.py). Script dùng dữ liệu synthetic, database tạm và Redis giả ném đúng exception của thư viện; không kết nối Redis thật, gọi nhà cung cấp thời tiết, gửi cảnh báo hay sửa database vận hành.
- Đây là review xuyên suốt các phân hệ và hợp đồng tích hợp, không phải chứng nhận mọi dòng code, mọi dữ liệu hoặc mọi cấu hình triển khai đều đã được kiểm chứng.

P1: cần giải quyết trước khi nghiệm thu/triển khai luồng bị ảnh hưởng. P2: lỗi cần sửa trong vòng ổn định tiếp theo, có điều kiện kích hoạt hoặc phạm vi hẹp hơn.

## Kết quả chạy thực tế

| Kiểm tra | Kết quả ngày 23/09/2026 |
| --- | --- |
| Backend pytest | **235 passed, 1 skipped**, 3 warnings; 68,03 giây |
| PostGIS thật | Chưa chạy; skip vì thiếu `POSTGIS_TEST_URL` |
| Frontend Node tests | **15/15 passed** |
| TypeScript `npm run lint` | Pass; script này thực tế là `tsc --noEmit` |
| Frontend production build | Pass; 1.923 modules; đầu ra riêng trong `.pytest-temp/review-20260923-dashboard` |
| Flake8 `src tests` | Pass |
| isort `--check-only src tests` | Pass |
| Black `--check src tests` | **Fail**: `src/typhoon_vn/api/app.py`, `tests/test_api_auth.py` |
| `pip check` | Không có dependency Python bị hỏng |
| Plan validator | Pass: 818/818 checkbox, 731 nodes, 3.237 links |
| Build wheel | Pass; nhưng wheel thiếu tài nguyên migration và không khởi tạo Store được |
| Probe hành vi ngoài test suite | Xác nhận các lỗi dữ liệu, migration, cache, metadata, API contract mô tả bên dưới |

Báo cáo pytest: [review-20260923-pytest.xml](review-20260923-pytest.xml). Ba warnings liên quan Starlette/httpx/AnyIO và tính năng nested tensor của PyTorch; không phải test failure.

Lệnh chạy pytest ban đầu có lỗi quoting ở phần đặt biến `DEBUG` trong PowerShell lồng nhau; pytest vẫn chạy đến hết và trả exit code 0. Không coi phần đặt biến đó là thành công. Script tái hiện đặt `DEBUG=false` trực tiếp trong tiến trình Python của nó.

Plan validator chỉ kiểm tra cấu trúc kế hoạch/liên kết và tự ghi lại `docs/planning/plan_validation.json`. Trường `product_tests_run_this_turn: false` trong output là giá trị hard-code của validator, không mô tả bộ pytest đã chạy riêng trong review này.

## Các phát hiện cần xử lý

### R01 — P1: Scaler làm thay đổi cả tọa độ mục tiêu của training

**Vị trí:** `src/typhoon_vn/datasets/typhoon_dataset.py:94–95,143–145`; `training/pipeline.py:310–314`.

`FEATURE_COLUMNS` có cả `lat` và `lon`. Dataset ghi dữ liệu đã chuẩn hóa trở lại cùng DataFrame rồi lấy `y_reg` từ chính các cột đó. Mô hình được huấn luyện dự đoán tọa độ đã chuẩn hóa; `predict_bundle()` lại đọc trực tiếp đầu ra thành độ vĩ/kinh, không inverse-transform. Các loss/metric khoảng cách cũng hiểu các giá trị này như tọa độ địa lý.

**Đã tái hiện:** cùng một mẫu có nhãn thô `[15.716047, 126.379066]`, nhưng khi truyền scaler thì nhãn thành `[0.652793, 1.150835]`. Đây không chỉ là khác biệt scale của input. Tọa độ sai vẫn có thể nằm trong giới hạn WGS84, nên validation biên không phát hiện được.

**Cần sửa:** tách ma trận features đã scale khỏi target địa lý; hoặc định nghĩa đầy đủ target transform và inverse trong loss/evaluation/serving. Thêm test target không đổi khi bật input scaler và một test train→bundle→forecast kiểm tra đơn vị tọa độ. Đánh giá lại artifact đã train bằng đường đi này trước khi sử dụng.

### R02 — P1: Backtest không dùng preprocessing đã fit khi train

**Vị trí:** `src/typhoon_vn/evaluation/backtest.py:34–67`; đối chiếu `training/run.py` và `training/pipeline.py:302`.

`backtest_storm()` tự tạo `TyphoonDataset` không có scaler; API hàm cũng không nhận bundle/scaler. Trong khi đó, training và serving bundle đều chuẩn hóa input bằng scaler đã fit. Gọi backtest với model lấy từ bundle sẽ đưa feature thô vào model đã học feature chuẩn hóa, làm số đo đánh giá không đại diện cho đường serving.

**Đã tái hiện:** hai feature đầu của cùng fix là `[15.739560, 126.583176]` ở input backtest, nhưng `[0.728782, 1.233133]` ở input training. Probe dùng model ghi lại tensor nhận được, không cần train thêm.

**Cần sửa:** backtest nhận và dùng preprocessing của bundle; giữ nhánh baseline có hợp đồng riêng. Thêm kiểm tra tensor và dự đoán của backtest trùng với serving trên cùng cửa sổ. Lỗi này độc lập với R01: sửa target vẫn chưa sửa input của backtest.

### R03 — P1: Nâng cấp database cũ thất bại khi khởi động

**Vị trí:** `src/typhoon_vn/operations/store.py:191–197`; `migrations/versions/0001_operational_schema.py`.

Database do main tạo có bảng nghiệp vụ và `schema_versions`, nhưng không có revision Alembic. Store mới luôn chạy upgrade; migration đầu tiên tạo lại bảng đã tồn tại.

**Đã tái hiện:** tạo SQLite tạm bằng metadata lấy trực tiếp từ `main:src/typhoon_vn/operations/store.py`, rồi mở bằng Store hiện tại: `OperationalError: table typhoons already exists`.

**Cần sửa:** đường nâng cấp nhận diện schema cũ, chuyển đổi dữ liệu và backfill cột/khóa trước khi ghi revision. Không chỉ stamp revision mới lên schema cũ vì cấu trúc khác nhau. Kiểm thử bảo toàn observations, forecasts, subscriptions, alerts và khả năng mở lại sau migration.

### R04 — P1: Redis outage làm hỏng cả forecast cache và weather cache

**Vị trí:** `operations/cache.py:100,112,131,148`; `weather/cache.py:27,50`; `api/app.py:426,470`.

Các adapter không bắt `redis.exceptions.RedisError`. Connection/timeout exceptions của Redis không thuộc các nhóm `OSError`/`RuntimeError` đang bắt. Vì cache mặc định bật, lỗi xảy ra trước fallback database hoặc memory.

**Đã tái hiện:** fake client ném `redis.exceptions.ConnectionError` làm lỗi thoát khỏi đọc, ghi, invalidate storm/model. Weather cache cũng lỗi ngay cả khi có giá trị memory hợp lệ. Test hiện có trong `tests/test_cache.py` dùng `OSError`, nên chưa mô phỏng đúng lỗi Redis thật.

**Cần sửa:** bắt exception Redis phù hợp ở tất cả thao tác, giữ khả năng phân biệt lỗi serialize/lỗi lập trình, thêm test ConnectionError/TimeoutError và API test chứng minh dữ liệu durable vẫn phục vụ khi Redis hỏng.

### R05 — P1: Wheel không chứa migration; đường dẫn còn phụ thuộc cwd

**Vị trí:** `operations/store.py:156–160,169`; `alembic.ini:2`; `pyproject.toml:87–88`.

Store tìm `alembic.ini` bằng `parents[3]`; package-data chỉ khai báo dashboard. Với source checkout, `script_location = migrations` vẫn được giải tương đối theo cwd. Docker hiện cài editable và copy migrations thủ công nên có thể che lỗi của wheel thông thường.

**Đã tái hiện hai trường hợp:**

- Đổi cwd sang thư mục tạm, mở Store: `Path doesn't exist: migrations`.
- Build wheel, kiểm tra archive thấy không có tài nguyên migrations/alembic.ini; giải nén wheel, import mã package đó trong tiến trình Python riêng với `-I`, ngoài repo: `No 'script_location' key found in configuration`.

**Cần sửa:** đóng gói migration cùng package và cấu hình script location tuyệt đối theo package. Gate cần chạy mã từ wheel ở cwd khác repo. Probe hiện dùng wheel giải nén với dependency trong venv, chưa phải một lần cài toàn bộ dependency vào venv sạch.

### R06 — P1: Weather panel gọi endpoint chỉ có ở Pages, không có ở FastAPI

**Vị trí:** `viz/frontend/src/services/api.ts:89`; weather routes trong `src/typhoon_vn/api/app.py`; `viz/frontend/functions/api/weather/[[path]].js`.

`fetchLocalWeather()` gọi `/api/weather/bundle`. FastAPI chỉ khai báo current/hourly/daily/alerts và locations/search. Vite/nginx đưa `/api` về FastAPI; việc build React không triển khai Pages Functions lên FastAPI.

**Đã tái hiện:** gọi `/api/weather/bundle?location_id=da-nang` vào FastAPI nhận **404**. Do đó panel thời tiết chi tiết lỗi trên đường chạy local/FastAPI/Docker, kể cả khi cấu hình provider đúng. Đây không phải lỗi thiếu API key nhà cung cấp.

**Cần sửa:** thống nhất contract giữa hai backend, bổ sung bundle endpoint hoặc để frontend tổng hợp các endpoint hiện hữu. Thêm integration test từ frontend API client tới FastAPI thật. Tương tự, `/api/ai/chat` cũng trả 404 trên FastAPI; AI cần được đánh dấu chỉ hỗ trợ Pages hoặc có adapter backend tương ứng.

### R07 — P1: Dashboard chưa có đường xác thực tới API production

**Vị trí:** `viz/frontend/src/services/api.ts:30–38,140–172`; `api/app.py:authorize`; `docker-compose.prod.yml:9–11`; `infra/docker/nginx.conf:7`.

Production yêu cầu API key hoặc bearer token, nhưng `fetchJson()` không gửi credential, UI không có login/token flow trong đường gọi này và nginx không bổ sung credential phía server. Luồng load active storms/track sẽ bị 401. Thêm nữa, nginx không proxy `/token`, nên endpoint login không tới FastAPI qua frontend origin.

**Đã tái hiện phần API:** `/typhoons/active` không header trả **401**; cùng request có key fixture hợp lệ trả **200**. Kết luận frontend/nginx dựa trên đối chiếu mã, chưa chạy Docker end-to-end.

**Cần sửa:** thiết kế login/session hoặc backend proxy có phạm vi quyền phù hợp, đồng bộ route `/token`, thêm test dashboard với production auth bật. Không đưa API key đặc quyền chung vào bundle `VITE_*` để chữa lỗi này.

### R08 — P2: Inference gán sai nguồn gốc bán kính uncertainty

**Vị trí:** `src/typhoon_vn/inference/service.py:170–172`; `training/run.py:196–213`.

Training smoke xuất bán kính heuristic và manifest ghi `illustrative heuristic; not calibrated coverage`. Inference bỏ qua `manifest.uncertainty_method`, luôn ghi `80th percentile validation radial error; not calibrated coverage` cho trained model. Đây là tuyên bố sai về cách tạo bán kính, dù vẫn có câu cảnh báo chưa calibrated.

**Đã tái hiện:** bundle fixture có metadata giống contract export trả về hai chuỗi trên khác nhau.

**Cần sửa:** chuyển metadata uncertainty từ manifest đã validate tới response, không gán nguồn validation nếu chưa có. Thêm test heuristic bundle và calibrated/validation-derived bundle cho metadata đúng nguồn.

### R09 — P2: Metadata feature/scaler đọc sai tên trường manifest

**Vị trí:** `src/typhoon_vn/inference/service.py:89–91`; `training/pipeline.py:128–138`.

Exporter lưu `feature_schema_sha256` và `files['scaler.json']`; inference tìm `feature_schema_fingerprint` và `scaler_sha256`. Với bundle đúng schema exporter, response trained-model sẽ ghi `feature_schema_version='baseline-motion-v1'`, `scaler_version='none'`.

**Đã tái hiện** bằng fixture manifest theo các trường của exporter. Audit/provenance bị sai; không thể dùng hai trường response để xác nhận preprocessing thực tế.

**Cần sửa:** một schema manifest dùng chung và test export→load→API kiểm tra hash chính xác, tránh fallback âm thầm khi trained bundle thiếu metadata bắt buộc.

### R10 — P2: Bundle export lấy trọng số epoch cuối, không lấy checkpoint tốt nhất

**Vị trí:** `src/typhoon_vn/training/run.py:194–202`; `training/trainer.py:211–218`.

Trainer lưu `best.pt` khi validation cải thiện nhưng không restore model trước khi trả về. `run_training()` export ngay object model còn giữ epoch cuối. Khi early stopping hoặc epoch cuối kém hơn best epoch, bundle triển khai không khớp mô hình được lựa chọn theo validation.

**Mức chứng cứ:** xác định bằng đường điều khiển của mã; chưa chạy một training dài riêng để tạo tình huống validation giảm rồi tăng.

**Cần sửa:** load trọng số best trước export hoặc công bố rõ policy chọn last. Test có validation loss điều khiển và so sánh trọng số bundle với checkpoint được chọn.

### R11 — P2: Promotion gate chấp nhận NaN

**Vị trí:** `src/typhoon_vn/training/registry.py:27–34`.

Gate chỉ so sánh lớn hơn/nhỏ hơn. NaN khiến cả hai so sánh false, nên chất lượng không xác định vẫn qua gate. Coverage ngoài miền hợp lệ và metric âm cũng chưa được kiểm tra đầy đủ.

**Đã tái hiện:** `PromotionPolicy(100, 0.8).validate({'mean_error_km': nan, 'calibration_coverage': nan})` trả bình thường. Chưa thực hiện promotion thật trong review.

**Cần sửa:** metric và ngưỡng phải finite; error không âm; coverage trong `[0,1]`. Thêm test NaN, infinity, miền giá trị và chứng minh registry không đổi stage khi gate từ chối.

### R12 — P2: Worker và API tính Redis key khác nhau

**Vị trí:** `src/typhoon_vn/operations/worker.py:61–66`; `api/app.py:421–424`.

Worker đưa `result.input_revision` là chuỗi digest vào `cache.key()`, API đưa toàn bộ request dict. Cache tiếp tục hash đầu vào nên hai key khác nhau cho cùng forecast. Worker cache write không được API sử dụng.

**Đã tái hiện:** sau `update(..., cache=...)`, Redis fixture có một forecast entry nhưng key API sẽ đọc không tồn tại. Database fallback vẫn hoạt động khi Redis khỏe; đây chủ yếu là lỗi tích hợp/hiệu năng.

**Cần sửa:** dùng một helper tạo input revision và key thống nhất, test worker ghi→API hit mà không gọi forecast lại.

### R13 — P2: Worker CLI không nối cache invalidation

**Vị trí:** `src/typhoon_vn/operations/worker.py:169–175,202–212`; `api/app.py:466–475`.

Compose truyền `REDIS_URL` cho worker, nhưng `main()`/`run_worker()` không tạo cache và gọi `update()` không có cache. API đang cache danh sách active storms có thể tiếp tục trả danh sách cũ sau khi worker ghi quan trắc mới, tối đa TTL mặc định 1.800 giây. Sửa key ở R12 chưa giải quyết được việc worker CLI không dùng cache.

**Mức chứng cứ:** đối chiếu luồng entrypoint/compose; chưa chạy worker+Redis thật.

**Cần sửa:** nối lifecycle Redis/cache vào entrypoint, invalidate active-list và storm khi thay đổi dữ liệu; thêm test đi qua chính entrypoint hoặc run_worker, không chỉ helper `update()`.

### R14 — P2: Prometheus production không có credential để scrape `/metrics`

**Vị trí:** `infra/monitoring/prometheus.yml:5–9`; `api/app.py:402`; `docker-compose.prod.yml`.

`/metrics` dùng `authorize`, còn scrape config chỉ có target/path, không có authorization/API-key configuration. Trong production auth bắt buộc, scrape sẽ nhận 401 và không thu metrics ứng dụng.

**Đã tái hiện phần API:** `/metrics` không credential trả **401**. Chưa chạy Prometheus container thật.

**Cần sửa:** credential riêng cho monitoring qua secret và cơ chế auth được hỗ trợ, hoặc endpoint nội bộ được kiểm soát truy cập. Kiểm tra target UP và sample thực sau deploy, không chỉ parse compose.

### R15 — P2: Gate Black hiện thất bại

**Vị trí:** `src/typhoon_vn/api/app.py`, `tests/test_api_auth.py`; `.github/workflows/ci.yml:25`.

**Đã chạy:** Black báo 2 file cần format, 131 file giữ nguyên. Workflow hiện chạy cùng gate nên trạng thái working tree này chưa đạt CI, dù pytest/flake8/isort pass.

**Cần sửa:** format đúng hai file, giữ thay đổi đang có của người dùng, rồi chạy lại gate. Review này chưa tự format code.

## Đánh giá theo phân hệ

| Phân hệ | Điểm tốt đã thấy trong mã/test | Giới hạn hoặc ưu tiên |
| --- | --- | --- |
| Ingestion/provenance | Streaming download, checksum, retry/circuit, chuẩn hóa nguồn, test fixture | Chưa kiểm tra credential/quota/schema hiện tại của nguồn thật |
| Features/datasets | FeatureBuilder dùng chung; split theo cả storm/năm; scaler fit trên training; kiểm tra time window | R01 phá hợp đồng đơn vị target; coverage hiện chưa bắt được |
| Models/training | LSTM/Seq2Seq/Attention/Transformer; checkpoint/RNG; strict bundle allowlist/checksum | R10 chọn trọng số export; smoke synthetic chưa chứng minh forecast skill |
| Evaluation/registry | Metric, seasonal folds, sealed-test helpers, promotion/rollback | R02 preprocessing backtest; R11 dữ liệu metric không hữu hạn |
| Inference | Kiểm tra time/motion, cache có giới hạn, phân biệt baseline/trained và disclaimer | R01, R08, R09; cần kiểm thử end-to-end bằng bundle thật |
| API/auth | Validation, request ID, lỗi có cấu trúc, API key/JWT, production validation | R07 tích hợp dashboard; rate limiter trong process không phải quota chia sẻ đa replica |
| Storage/operations | Alembic, FK/index, upsert, revision quan trắc, lưu forecast và draft | R03–R05, R12–R14; PostGIS thật chưa kiểm chứng lại trong phiên |
| Weather | Provider adapters, TTL/stale fallback, lỗi có kiểu | R04 và R06; hai backend Python/Pages đã lệch contract |
| Alerts/webhooks | Draft-only, idempotency/cooldown, helpers ký payload/kiểm tra destination | Kênh thực đang disabled/fake; chưa chứng minh delivery thật hoặc retry bền vững qua restart |
| Frontend/map | TypeScript/build/tests pass; demo tách rõ, lỗi API không tự đổi sang dữ liệu demo; map/layer components | R06/R07; chưa browser QA trực quan, keyboard/screen reader hay thiết bị thật |
| Packaging/deployment/CI | Có Dockerfiles/compose/CI/monitoring và package metadata | R05, R14, R15; CI frontend chưa chạy `npm test`, hiện chỉ lint/build |
| Docs/planning | Roadmap có traceability; validator pass; README nêu rõ chưa production-ready | Số liệu README 209 tests, progress lịch sử 232 tests khác kết quả hiện tại 235; không dùng số lịch sử làm bằng chứng hiện tại |

## Những rủi ro/chỗ thiếu bằng chứng, chưa xếp thành lỗi đã tái hiện

- `forecast_cache_max_entries` và `inference_max_concurrency` có trong Settings nhưng chưa thấy được truyền/áp dụng trong `create_app()`. Nên làm rõ cấu hình nào thực sự có tác dụng và đo tải trước khi đặt SLA.
- Redis forecast hit trả response ngay, trong khi durable-cache hit mới bổ sung cảnh báo quan trắc quá 24 giờ. Cần test cache qua ranh giới freshness.
- Database `active()` đọc toàn bộ storm rồi query track từng storm; cần profile theo dung lượng vận hành trước khi kết luận đạt hiệu năng.
- `BackupManager` là file copy/checksum. Chưa có chứng cứ phiên này rằng backup database đang ghi/WAL hoặc PostgreSQL đáp ứng RPO/RTO; cần drill đúng công cụ và loại database thực tế.
- Các helper environmental availability, calibration, alert delivery và release policy không tự chứng minh đã nối vào tất cả entrypoint production.
- Không kiểm tra lỗ hổng dependency bằng advisory online/npm audit trong phiên này. `pip check` chỉ xác nhận tương thích dependency, không phải chứng nhận an toàn bảo mật.
- Không chạy lại Docker, PostGIS, Redis, live weather, Ollama, public Pages, load test hoặc gửi cảnh báo. Không coi các evidence lịch sử trong repo là kết quả chạy mới.
- Không đủ chứng cứ kết luận có rò rỉ credential; review không đưa nội dung `.env` hay secret vào báo cáo. Những biến Vite public cần được quản lý đúng vai trò frontend.

## Thứ tự xử lý đề xuất

1. **Đúng dữ liệu trước:** R01, R02; thêm test đơn vị tọa độ và parity backtest/serving, đánh giá lại model artifact liên quan.
2. **Khởi động và chịu lỗi:** R03, R04, R05; test legacy migration có dữ liệu, cache outage với Redis exceptions thật, wheel ngoài repo.
3. **Luồng người dùng hoàn chỉnh:** R06, R07; thống nhất API contract và kiểm thử frontend→nginx→FastAPI với auth bật.
4. **Đúng nguồn gốc/kết quả mô hình:** R08–R11; metadata, checkpoint selection và promotion gates.
5. **Vận hành và CI:** R12–R15; worker cache, metrics auth, formatting; bổ sung frontend tests vào CI.
6. Chạy lại full suite và integration thực trong môi trường cấu hình riêng, sau đó cập nhật evidence và nghiệm thu. Hosting/credential/approval là các điều kiện bổ sung; chúng không thay thế việc sửa lỗi code trên.

## Tái chạy và artefact của review

Chạy từ thư mục gốc project:

```powershell
rtk proxy .venv/Scripts/python.exe -m pytest -q --basetemp=.pytest-temp/review-20260923-rerun --junitxml=reports/review-20260923-rerun-pytest.xml
rtk proxy .venv/Scripts/python.exe -m pip wheel . --no-deps --no-build-isolation --wheel-dir .pytest-temp/review-20260923-wheel
rtk proxy .venv/Scripts/python.exe reports/review-20260923-reproduce.py
rtk proxy .venv/Scripts/python.exe -m flake8 src tests
rtk proxy .venv/Scripts/python.exe -m isort --check-only src tests
rtk proxy .venv/Scripts/python.exe -m black --check src tests
rtk proxy .venv/Scripts/python.exe -m pip check
```

Trong `viz/frontend`:

```powershell
rtk proxy npm.cmd test
rtk proxy npm.cmd run lint
rtk proxy npm.cmd run build -- --outDir ../../.pytest-temp/review-20260923-dashboard
```

Script probe **in ra hành vi đang quan sát**, không phải regression test khẳng định phần mềm đúng; exit code 0 của script không có nghĩa các lỗi đã được sửa. Trường `returned: null` của promotion probe nghĩa là validator không ném lỗi với NaN. Phần wheel chỉ chạy khi đã build wheel ở thư mục chỉ định. Nhánh legacy cần còn Git ref `main` chứa schema được đối chiếu.

Artefact chính: báo cáo này, script tái hiện và JUnit XML. Các kiểm tra sinh thêm test/build artifacts trong `.pytest-temp`, wheel/build metadata, và validator làm mới `docs/planning/plan_validation.json`. Không sửa code nghiệp vụ, không reset/stage/commit/push, không nâng cấp database vận hành hoặc deploy.
