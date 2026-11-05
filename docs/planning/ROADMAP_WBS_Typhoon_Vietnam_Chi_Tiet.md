# ROADMAP XÂY DỰNG HỆ THỐNG HỖ TRỢ GỢI Ý ĐƯỜNG ĐI BÃO VIỆT NAM

> Phát triển từ repo mẫu: `VietManh05/typhoon-track-vietnam` (LSTM 1 bước, CMA Best Track, Cartopy)
> Mục tiêu: hệ thống hoàn chỉnh production-ready — dữ liệu → mô hình → API → dashboard → cảnh báo → triển khai.

---

## 0. Đánh giá repo mẫu (điểm xuất phát)

| Thành phần Hiện trạng trong repo mẫu Hạn chế cần khắc phục  |                                                       |                                                                                       |
| ----------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `data_clean.py`                                             | Parse file `.txt` CMA Best Track → `cleaned_data.csv` | Chỉ 1 nguồn (CMA), chưa có dữ liệu VN (NCHMF), chưa merge SST/khí áp môi trường       |
| `share_func.py`                                             | Haversine, bearing, normalize, one-hot                | Min-max theo *toàn bộ* dữ liệu (rò rỉ thông tin train/test), thiếu chuẩn hoá theo mùa |
| `data_loader.py`                                            | `TyphoonDataset` cắt chuỗi 4 điểm → 1 điểm kế tiếp    | Không tách theo cơn bão khi train/val split (rò rỉ), chỉ dự đoán 1 bước               |
| `model.py`                                                  | LSTM đơn giản, 1 lớp FC                               | Không có attention, không multi-horizon, không ước lượng độ bất định                  |
| `train.py`                                                  | Vòng lặp huấn luyện cơ bản, lưu best checkpoint       | Không có early stopping, không log (TensorBoard/W&B), không cross-validation          |
| `predict.py`                                                | Dự đoán tuần tự 1 bước, so khớp thực tế               | Không có API, không hỗ trợ dự báo nhiều bước tương lai (24h/48h/72h)                  |
| `draw_map.py`                                               | Vẽ bản đồ tĩnh + GIF bằng Cartopy                     | Không tương tác, không phải web dashboard                                             |
| Không có                                                    | —                                                     | Backend API, frontend, cảnh báo, CI/CD, kiểm thử, giám sát mô hình                    |

➡️ Roadmap dưới đây giữ lại ý tưởng lõi (LSTM + đặc trưng chu kỳ + Haversine/bearing) nhưng mở rộng thành hệ thống hoàn chỉnh.

---

## 1. Kiến trúc tổng thể

```
[Nguồn dữ liệu thô]        [Data Pipeline]         [ML Service]           [Backend API]        [Frontend]        [Cảnh báo]
CMA / JTWC / JMA    -->   ETL + Feature Store  -->  Train/Eval/Registry -->  FastAPI inference --> Web Dashboard --> SMS/Email/Push
NCHMF (VN) / ERA5                                   (multi-horizon LSTM/                          (bản đồ Leaflet/                 Webhook/Zalo/Telegram
GFS/ECMWF (tuỳ chọn)                                Transformer + ensemble)                        Mapbox + cone bất định)

```

Nguyên tắc thiết kế:

- **Tách rời từng module** (data, model, serving, UI) để có thể phát triển/kiểm thử độc lập.
- **Có thể tái huấn luyện định kỳ** khi có dữ liệu bão mới trong mùa.
- **Ước lượng độ bất định** (cone of uncertainty) thay vì chỉ 1 đường đi đơn — đúng bản chất "gợi ý", không phải khẳng định.
- **Ưu tiên khu vực ảnh hưởng Việt Nam** (Biển Đông, 5°–24°N, 100°–125°E) khi lọc/gán nhãn.

---

## 2. GIAI ĐOẠN 0 — Chuẩn bị & thiết lập môi trường

### 2.1 Khởi tạo repo & quy ước dự án

- [ ] Fork/clone `typhoon-track-vietnam` làm base, tạo repo mới `typhoon-vn-forecast-system`
- [ ] Thiết lập cấu trúc thư mục chuẩn: 
  ```
  /data (raw/, interim/, processed/, external/)/notebooks/src  /ingestion  /features  /models  /training  /inference  /api  /viz/frontend/infra (docker, k8s, terraform)/tests/docs

  ```
- [ ] Viết `README.md` gốc mô tả kiến trúc (sơ đồ ở mục 1)
- [ ] Tạo `.gitignore` (loại trừ `data/raw`, `checkpoints/*.pth`, `.env`)
- [ ] Chọn license (giữ MIT như repo gốc) + `CONTRIBUTING.md`
- [ ] Thiết lập quy ước commit (Conventional Commits) + pre-commit hook (black, isort, flake8)

### 2.2 Môi trường phát triển

- [ ] Chọn Python version cố định (vd 3.11), tạo `pyproject.toml`/`poetry.lock` thay cho `requirements.txt` rời rạc
- [ ] Tách `requirements-train.txt` (torch, cartopy) và `requirements-api.txt` (fastapi, uvicorn) để image nhẹ hơn
- [ ] Viết `Makefile`/`justfile` với các lệnh: `make setup`, `make clean-data`, `make train`, `make serve`, `make test`
- [ ] Cấu hình biến môi trường qua `.env` + `pydantic-settings` (đường dẫn data, model registry, API keys)
- [ ] Thiết lập Docker Compose dev (Python service + Postgres/PostGIS + Redis + MinIO cho lưu checkpoint)

### 2.3 Quản lý thử nghiệm & dữ liệu

- [ ] Cài đặt DVC (Data Version Control) hoặc lakeFS để version hoá `cleaned_data.csv` và các checkpoint
- [ ] Cài đặt MLflow hoặc Weights & Biases để log experiment (loss, hyperparameter, artifact)
- [ ] Tạo bảng theo dõi thí nghiệm (spreadsheet/Notion) đối chiếu với MLflow run ID

---

## 3. GIAI ĐOẠN 1 — Thu thập & mở rộng dữ liệu

### 3.1 Giữ nguồn CMA Best Track (đã có trong repo mẫu)

- [ ] Viết script tải tự động toàn bộ `CMABSTdata/*.txt` từ CMA (thay vì thao tác tay), có retry + checksum
- [ ] Parse lại toàn bộ lịch sử (1949–hiện tại), không giới hạn 1 năm
- [ ] Chuẩn hoá `typhoonID` thành định dạng quốc tế (vd theo JTWC ID) để dễ đối chiếu đa nguồn

### 3.2 Bổ sung nguồn dữ liệu quốc tế

- [ ] Tích hợp **IBTrACS** (NOAA, tổng hợp đa cơ quan JTWC/JMA/CMA/HKO) làm nguồn chuẩn hoá chính
- [ ] Tích hợp **JMA Best Track** (Cơ quan Khí tượng Nhật Bản) làm nguồn đối chiếu chéo
- [ ] Tích hợp **JTWC Best Track** (Mỹ) cho các cơn bão ở Tây Bắc Thái Bình Dương
- [ ] Viết module hợp nhất (`merge_sources.py`) xử lý trùng lặp/khác biệt giữa các nguồn (theo thời gian + vị trí gần nhau)

### 3.3 Dữ liệu đặc thù Việt Nam

- [ ] Thu thập dữ liệu công báo bão của **Trung tâm Dự báo KTTV Quốc gia (NCHMF)** — bản tin lịch sử, vị trí tâm bão theo giờ VN
- [ ] Thu thập dữ liệu thiệt hại/đổ bộ lịch sử (tỉnh/thành bị ảnh hưởng) từ Ban Chỉ đạo PCTT để làm tập nhãn phụ (impact labeling)
- [ ] Số hoá ranh giới hành chính Việt Nam (GADM/OpenStreetMap) phục vụ tính "khoảng cách tới bờ biển VN gần nhất"
- [ ] Thu thập dữ liệu đường bờ biển chi tiết (GSHHG) cho việc tính landfall (đổ bộ)

### 3.4 Dữ liệu môi trường hỗ trợ (features vật lý)

- [ ] Tải **SST (nhiệt độ mặt nước biển)** từ NOAA OISST — bão cần SST > 26.5°C để duy trì cường độ
- [ ] Tải dữ liệu tái phân tích **ERA5** (ECMWF): áp suất mực biển, gió 850hPa/200hPa (shear gió), độ ẩm
- [ ] (Tuỳ chọn nâng cao) Tải trường dự báo số trị **GFS/ECMWF** để làm đặc trưng bổ sung theo thời gian thực khi inference
- [ ] Viết pipeline crawl + cache dữ liệu môi trường theo lưới lat/lon/thời gian khớp với vị trí bão

### 3.5 Lưu trữ dữ liệu thô

- [ ] Thiết kế schema lưu trữ thống nhất (Parquet, phân vùng theo năm) trong `/data/raw`
- [ ] Viết job lịch (cron/Airflow) để tự động cập nhật dữ liệu mùa bão mới hàng tuần/hàng ngày trong mùa bão (6–11 hàng năm)
- [ ] Ghi log nguồn gốc (data lineage) cho mỗi bản ghi: nguồn, thời gian tải, phiên bản

---

## 4. GIAI ĐOẠN 2 — Làm sạch & Feature Engineering nâng cao

### 4.1 Làm sạch dữ liệu (kế thừa & mở rộng `data_clean.py`)

- [ ] Tái cấu trúc `data_clean.py` thành pipeline theo bước rõ ràng (parse → validate → dedupe → merge → export)
- [ ] Viết bộ validate: toạ độ hợp lệ (VN quan tâm 0–30°N, 100–140°E), áp suất 850–1050 hPa, tốc độ gió ≥ 0
- [ ] Xử lý giá trị thiếu bằng nội suy theo chuỗi thời gian của từng cơn bão (không dùng 0 mặc định như bản gốc)
- [ ] Loại bỏ/gắn cờ các bản ghi trùng lặp giữa nguồn CMA/JMA/JTWC/IBTrACS (ưu tiên IBTrACS đã hợp nhất)
- [ ] Chuẩn hoá đơn vị nhất quán (m/s vs knot cho gió; hPa cho áp suất) giữa các nguồn khác nhau

### 4.2 Đặc trưng không gian – thời gian (kế thừa `share_func.py`)

- [ ] Giữ và kiểm thử lại hàm `haversine`, `calculate_bearing`, `calculate_new_position` bằng unit test (so khớp giá trị đã biết)
- [ ] Thêm đặc trưng **tốc độ di chuyển** (km/h) và **gia tốc thay đổi hướng** (Δbearing/Δt)
- [ ] Thêm đặc trưng **khoảng cách & bearing tới đường bờ biển Việt Nam gần nhất**
- [ ] Thêm đặc trưng **khoảng cách tới các mốc địa lý** (Hoàng Sa, Trường Sa, các cảng chính) — hỗ trợ diễn giải cho người dùng
- [ ] Giữ biến đổi chu kỳ sin/cos cho giờ/ngày/tháng/ngày-trong-năm (như bản gốc) nhưng thêm **chu kỳ mùa bão** (tháng 6–12 là mùa cao điểm)

### 4.3 Đặc trưng cường độ & môi trường

- [ ] Chuẩn hoá lại `I` (cấp độ) và `END` theo one-hot **cố định danh sách lớp** (không suy ra động từ dữ liệu để tránh lệch chiều giữa train/test)
- [ ] Thêm đặc trưng SST tại vị trí tâm bão + gradient SST xung quanh
- [ ] Thêm đặc trưng wind shear (chênh lệch gió 850hPa–200hPa) — yếu tố quan trọng cho cường độ hoá/suy yếu
- [ ] Thêm đặc trưng khí áp môi trường xung quanh (áp cao cận nhiệt đới chi phối hướng đi)

### 4.4 Chuẩn hoá đúng cách (khắc phục lỗi rò rỉ dữ liệu trong bản gốc)

- [ ] Tính min-max/mean-std **chỉ trên tập train**, lưu lại scaler (pickle/json) để áp dụng cho val/test/inference
- [ ] Viết class `FeatureScaler` để đảm bảo `normalize`/`denormalize` dùng chung tham số đã fit, không tính lại mỗi lần
- [ ] Đóng gói toàn bộ bước feature engineering thành `sklearn.Pipeline`-style hoặc custom `FeatureBuilder` để tái sử dụng giữa training và serving

### 4.5 Feature Store

- [ ] Thiết lập feature store đơn giản (Parquet có versioning hoặc Feast) để đảm bảo tính nhất quán train/serve
- [ ] Viết script kiểm tra "schema drift" khi có cột mới/thiếu giữa các lần chạy

---

## 5. GIAI ĐOẠN 3 — Thiết kế lại Dataset & mô hình

### 5.1 Dataset đa bước (khắc phục giới hạn dự đoán 1 bước của bản gốc)

- [ ] Viết lại `TyphoonDataset` hỗ trợ **cửa sổ trượt cấu hình được** (không cố định 4 bước input)
- [ ] Hỗ trợ **dự đoán nhiều bước tương lai (multi-horizon)**: 6h, 12h, 24h, 48h, 72h — giống sản phẩm dự báo thực tế
- [ ] Sửa lỗi tách train/val: chia theo **typhoonID** (toàn bộ 1 cơn bão vào 1 tập), không chia theo index tuần tự để tránh rò rỉ
- [ ] Thêm tuỳ chọn chia theo **năm** (train các năm cũ, validate/test năm gần nhất) mô phỏng kịch bản triển khai thực tế
- [ ] Viết `collate_fn` xử lý chuỗi độ dài khác nhau (padding + mask) nếu dùng kiến trúc attention

### 5.2 Nâng cấp kiến trúc mô hình

- [ ] **Baseline**: giữ nguyên `TropicalCycloneLSTM` (bản gốc) làm mốc so sánh
- [ ] **Seq2Seq LSTM (Encoder-Decoder)**: dự đoán chuỗi nhiều bước thay vì 1 điểm
- [ ] **LSTM + Attention**: cho phép mô hình tập trung vào các điểm lịch sử quan trọng
- [ ] **Transformer nhỏ (Temporal Fusion Transformer hoặc Informer-lite)**: thử nghiệm cho chuỗi dài & nhiều đặc trưng ngoại sinh (SST, shear)
- [ ] **Mô hình vật lý kết hợp (hybrid)**: dùng CLIPER (Climatology and Persistence) làm baseline cổ điển để so sánh với deep learning
- [ ] Tách output thành 2 đầu riêng: **hồi quy vị trí** (lat/lon hoặc distance/bearing) và **phân loại cường độ/trạng thái** (thay vì gộp chung 1 vector loss như bản gốc)

### 5.3 Ước lượng độ bất định ("cone of uncertainty")

- [ ] Thử **Monte Carlo Dropout** khi inference để sinh nhiều đường đi khả dĩ
- [ ] Thử **Quantile Regression** (dự đoán khoảng tin cậy 10–90%) cho vị trí tương lai
- [ ] Thử **Deep Ensemble** (huấn luyện N mô hình với seed khác nhau, lấy phân phối)
- [ ] Viết hàm tính bán kính "cone" theo horizon (giống cách NHC/NCHMF công bố vùng có thể ảnh hưởng)

### 5.4 Hàm mất mát & tối ưu

- [ ] Giữ `SmoothL1Loss` cho hồi quy vị trí (đã hợp lý trong bản gốc), nhưng tách trọng số riêng cho từng horizon (phạt nặng hơn ở bước xa)
- [ ] Thêm `CrossEntropyLoss` riêng cho phần phân loại cường độ/trạng thái
- [ ] Thử loss theo khoảng cách Haversine trực tiếp (thay vì lat/lon thô) để tối ưu đúng theo mét/km thực tế
- [ ] Giữ `AdamW` (đã hợp lý), thêm scheduler (CosineAnnealingLR hoặc ReduceLROnPlateau)

---

## 6. GIAI ĐOẠN 4 — Huấn luyện, đánh giá, MLOps

### 6.1 Vòng lặp huấn luyện nâng cấp (mở rộng `train.py`)

- [ ] Thêm **early stopping** (patience theo validation loss) thay vì chạy đủ `num_epochs` cố định
- [ ] Thêm **gradient clipping** để ổn định huấn luyện LSTM sâu
- [ ] Tích hợp logging vào MLflow/W&B (loss theo epoch, learning rate, sample dự đoán trực quan)
- [ ] Thêm checkpoint "last" và "best" riêng biệt, dọn dẹp checkpoint cũ tự động
- [ ] Hỗ trợ resume training từ checkpoint kèm optimizer state (bản gốc chỉ load `state_dict` của model)
- [ ] Viết cấu hình bằng YAML/Hydra thay vì chỉ `argparse` để dễ quản lý nhiều thí nghiệm

### 6.2 Đánh giá mô hình

- [ ] Định nghĩa metric chuẩn ngành: **Track error (km)** tại từng horizon (24h/48h/72h) — so sánh được với số liệu công bố của NCHMF/JTWC
- [ ] Tính **Along-track error** và **Cross-track error** riêng biệt (chuẩn khí tượng, không chỉ MSE thô)
- [ ] Tính độ chính xác phân loại cường độ (accuracy/F1 theo từng cấp bão)
- [ ] Viết script **backtesting** trên các cơn bão lịch sử ảnh hưởng Việt Nam nổi bật (vd Damrey 2017, Molave 2020, Noru 2022, Yagi 2024) để đánh giá định tính
- [ ] So sánh với baseline CLIPER và với dự báo chính thức đã công bố (nếu có dữ liệu) để biết mô hình có "ăn được" dự báo nghiệp vụ không

### 6.3 Kiểm định chéo & tinh chỉnh siêu tham số

- [ ] Thiết lập **cross-validation theo mùa bão** (leave-one-season-out) thay vì 1 lần chia 90/10 như bản gốc
- [ ] Dùng Optuna/Ray Tune để tìm `hidden_size`, `num_layers`, `dropout`, `learning_rate` tối ưu
- [ ] Phân tích độ nhạy của mô hình theo độ dài chuỗi input (4 điểm như bản gốc có đủ chưa? thử 6, 8 điểm)

### 6.4 Model Registry & CI cho mô hình

- [ ] Đăng ký mọi mô hình đạt ngưỡng chất lượng vào MLflow Model Registry (kèm metric, phiên bản dữ liệu)
- [ ] Viết quy tắc promote: "staging" → "production" chỉ khi track error thấp hơn mô hình hiện tại trên tập test cố định
- [ ] Tạo GitHub Actions job tự động chạy lại đánh giá khi có PR thay đổi model/feature code

---

## 7. GIAI ĐOẠN 5 — Dịch vụ suy luận & Backend API

### 7.1 Đóng gói inference (mở rộng `predict.py`)

- [ ] Tách logic inference khỏi script CLI, viết class `TyphoonForecaster` tái sử dụng được (load model 1 lần, serve nhiều request)
- [ ] Viết hàm "rolling forecast": từ 4 điểm quan trắc gần nhất, sinh dự báo 24h/48h/72h bằng cách feed lại chính đầu ra (autoregressive) — có kiểm soát sai số tích luỹ
- [ ] Tích hợp bước denormalize/restore bearing (giữ logic đã có trong `share_func.py`, đóng gói lại thành hàm `postprocess_prediction`)
- [ ] Thêm cơ chế fallback (nếu thiếu đặc trưng môi trường thời gian thực, dùng giá trị trung bình lịch sử)

### 7.2 Xây dựng API (FastAPI)

- [ ] Thiết kế endpoint `POST /forecast` — nhận `typhoonID` hoặc chuỗi quan trắc thô, trả về danh sách điểm dự báo + cone bất định
- [ ] Thiết kế endpoint `GET /typhoons/active` — danh sách bão đang hoạt động (từ nguồn dữ liệu cập nhật)
- [ ] Thiết kế endpoint `GET /typhoons/{id}/track` — lịch sử + dự báo của 1 cơn bão cụ thể
- [ ] Thiết kế endpoint `GET /typhoons/{id}/impact` — ước tính khu vực/tỉnh thành VN có khả năng ảnh hưởng (dựa khoảng cách + bán kính gió mạnh)
- [ ] Viết schema Pydantic cho request/response, sinh OpenAPI docs tự động
- [ ] Thêm health-check endpoint (`/health`) và version endpoint (`/version`) báo cáo model version đang chạy
- [ ] Thêm rate limiting & API key cơ bản nếu public hoá

### 7.3 Dữ liệu thời gian thực & cập nhật liên tục

- [ ] Viết worker (Celery/RQ) định kỳ (vd mỗi 30–60 phút trong mùa bão) kéo dữ liệu vị trí bão mới nhất từ NCHMF/JTWC
- [ ] Khi có điểm quan trắc mới, tự động trigger lại inference và lưu kết quả vào DB (Postgres/PostGIS)
- [ ] Thiết lập cache (Redis) cho các dự báo mới nhất để giảm tải tính toán lặp lại

### 7.4 Lưu trữ vận hành

- [ ] Thiết kế schema PostGIS: bảng `observations`, `forecasts`, `typhoons`, `alerts`
- [ ] Viết migration (Alembic) cho schema trên
- [ ] Lưu lịch sử mọi lần dự báo (audit trail) để sau này đánh giá lại độ chính xác thực tế

---

## 8. GIAI ĐOẠN 6 — Frontend Dashboard

### 8.1 Lựa chọn công nghệ

- [ ] Chọn framework (React/Next.js hoặc Vue) + thư viện bản đồ (Leaflet, Mapbox GL, hoặc deck.gl) — thay thế Cartopy tĩnh trong bản gốc bằng bản đồ tương tác
- [ ] Thiết kế hệ thống theme/màu (đỏ/cam/vàng theo cấp độ bão, giống chuẩn hiển thị của NCHMF)

### 8.2 Các màn hình chính

- [ ] **Trang tổng quan**: danh sách bão đang hoạt động ở Biển Đông/Tây Bắc Thái Bình Dương
- [ ] **Trang chi tiết bão**: bản đồ hiển thị đường đi lịch sử (đường liền) + đường đi dự báo (đường đứt) + cone bất định (vùng tô mờ mở rộng theo thời gian — tái hiện ý tưởng so sánh actual vs predicted của `draw_map.py` nhưng dạng tương tác)
- [ ] **Lớp phủ vùng ảnh hưởng Việt Nam**: highlight tỉnh/thành nằm trong bán kính cảnh báo
- [ ] **Timeline slider**: cho phép tua qua các thời điểm quan trắc/dự báo (giống hiệu ứng GIF gốc nhưng người dùng điều khiển được)
- [ ] **Bảng thông số**: áp suất, sức gió, cấp bão, hướng di chuyển tại thời điểm đang xem
- [ ] Responsive cho mobile (người dân vùng ảnh hưởng thường tra cứu bằng điện thoại)

### 8.3 Trải nghiệm người dùng bổ sung

- [ ] Cho phép nhập vị trí (tỉnh/thành hoặc toạ độ) để xem "khoảng cách còn lại tới bờ", "thời gian ước tính ảnh hưởng"
- [ ] Hiển thị mức độ tin cậy mô hình rõ ràng (disclaimer: đây là công cụ *hỗ trợ tham khảo*, không thay thế bản tin chính thức của NCHMF)
- [ ] Đa ngôn ngữ (Việt/Anh)

---

## 9. GIAI ĐOẠN 7 — Cảnh báo & tích hợp bên ngoài

### 9.1 Kênh cảnh báo

- [ ] Thiết kế cơ chế đăng ký nhận cảnh báo theo khu vực (email/SMS/Telegram bot/Zalo OA)
- [ ] Viết rule engine: kích hoạt cảnh báo khi bão dự báo vào bán kính X km quanh khu vực đăng ký trong Y giờ tới
- [ ] Viết template nội dung cảnh báo rõ ràng, có nguồn tham chiếu, khuyến cáo không thay thế cảnh báo chính thức
- [ ] Test cơ chế chống spam cảnh báo (throttle theo thời gian)

### 9.2 Tích hợp dữ liệu chính thống

- [ ] Đối chiếu song song dự báo của hệ thống với bản tin NCHMF để hiển thị "so sánh 2 nguồn" minh bạch cho người dùng
- [ ] Cân nhắc API/webhook để cơ quan phòng chống thiên tai địa phương có thể lấy dữ liệu (nếu dự án mở rộng quy mô)

---

## 10. GIAI ĐOẠN 8 — Kiểm thử

### 10.1 Unit test

- [ ] Test các hàm toán học trong `share_func.py` (haversine, bearing, calculate\_new\_position) với giá trị tham chiếu đã biết
- [ ] Test `FeatureBuilder`/scaler: đảm bảo normalize → denormalize khôi phục đúng giá trị gốc
- [ ] Test `TyphoonDataset`: đảm bảo không rò rỉ dữ liệu giữa các cơn bão/tập train-val
- [ ] Test model forward pass (shape đầu vào/ra đúng như kỳ vọng)

### 10.2 Integration test

- [ ] Test toàn bộ pipeline: raw data → cleaned → feature → dataset → train 1 epoch nhỏ → predict, chạy trong CI với dữ liệu mẫu nhỏ
- [ ] Test API end-to-end (gửi request `/forecast` mẫu, kiểm tra response schema + giá trị hợp lý)
- [ ] Test worker cập nhật dữ liệu thời gian thực (mock nguồn NCHMF)

### 10.3 Kiểm thử mô hình chuyên biệt

- [ ] Backtest trên tập cơn bão giữ lại hoàn toàn (không dùng để train/tune) — báo cáo track error theo horizon
- [ ] Test độ ổn định: nhiễu nhỏ đầu vào (vd sai số quan trắc) không làm output đổi đột ngột
- [ ] Test edge case: bão đổi hướng đột ngột, bão gần bờ, bão suy yếu thành áp thấp

### 10.4 Kiểm thử frontend

- [ ] Test hiển thị bản đồ với dữ liệu giả lập nhiều kịch bản (bão xa, bão gần, nhiều bão cùng lúc)
- [ ] Test responsive & accessibility cơ bản

---

## 11. GIAI ĐOẠN 9 — Triển khai & vận hành

### 11.1 Container hoá

- [ ] Viết Dockerfile riêng cho: training service, API service, worker, frontend
- [ ] Viết `docker-compose.prod.yml` (API + Postgres/PostGIS + Redis + Nginx reverse proxy)

### 11.2 CI/CD

- [ ] GitHub Actions: lint + unit test + build image khi push
- [ ] Pipeline riêng cho "retrain định kỳ" (vd đầu mỗi mùa bão) chạy trên GPU runner/cloud, tự động đăng ký model mới nếu vượt baseline
- [ ] Pipeline deploy tự động (staging → production) sau khi test pass

### 11.3 Hạ tầng & giám sát

- [ ] Chọn nền tảng triển khai (VPS Việt Nam để độ trễ thấp / cloud quốc tế có CDN) — cân nhắc tính sẵn sàng cao trong đúng mùa bão
- [ ] Thiết lập autoscaling cho API khi có bão lớn (traffic tăng đột biến)
- [ ] Giám sát hệ thống: Prometheus + Grafana (uptime, latency API, tỉ lệ lỗi worker cập nhật dữ liệu)
- [ ] Giám sát mô hình (model monitoring): theo dõi phân phối input thực tế có "trôi" (drift) so với lúc train không
- [ ] Thiết lập backup định kỳ cho DB và model registry

---

## 12. GIAI ĐOẠN 10 — Tài liệu hoá & bàn giao

- [ ] Cập nhật `README.md` chính với hướng dẫn cài đặt full-stack (data → train → serve → frontend)
- [ ] Viết tài liệu kiến trúc chi tiết (`docs/architecture.md`) kèm sơ đồ
- [ ] Viết tài liệu mô tả từng đặc trưng dữ liệu (data dictionary) — kế thừa và mở rộng phần "Lựa chọn đặc trưng" đã có trong README gốc
- [ ] Viết hướng dẫn vận hành (runbook): xử lý khi worker lỗi, khi model registry lỗi, khi có bão lớn tải cao
- [ ] Viết báo cáo đánh giá mô hình định kỳ theo mùa bão (post-season report), so sánh với thực tế đã xảy ra
- [ ] Viết tuyên bố miễn trừ trách nhiệm rõ ràng (công cụ tham khảo, không thay thế cơ quan khí tượng chính thức)
- [ ] Chuẩn bị slide/video demo bàn giao

---

## 13. Phụ lục A — Gợi ý mốc thời gian (indicative, điều chỉnh theo nguồn lực)

| Giai đoạn Nội dung Thời lượng gợi ý  |                                        |                       |
| ------------------------------------ | -------------------------------------- | --------------------- |
| 0                                    | Setup môi trường, quy ước dự án        | 3–5 ngày              |
| 1                                    | Thu thập & mở rộng dữ liệu             | 2–3 tuần              |
| 2                                    | Feature engineering nâng cao           | 1–2 tuần              |
| 3–4                                  | Thiết kế mô hình, huấn luyện, đánh giá | 3–4 tuần              |
| 5                                    | Backend API + inference service        | 1.5–2 tuần            |
| 6                                    | Frontend dashboard                     | 2–3 tuần              |
| 7                                    | Cảnh báo & tích hợp                    | 1 tuần                |
| 8                                    | Kiểm thử toàn diện                     | song song, xuyên suốt |
| 9                                    | Triển khai, CI/CD, giám sát            | 1–2 tuần              |
| 10                                   | Tài liệu hoá, bàn giao                 | 3–5 ngày              |

## 14. Phụ lục B — Rủi ro chính cần lưu ý

- [ ] **Chất lượng/độ trễ dữ liệu nguồn** (CMA/NCHMF có thể cập nhật chậm hoặc định dạng thay đổi) → cần cơ chế giám sát & cảnh báo khi pipeline ingestion lỗi
- [ ] **Sai số tích luỹ khi dự báo nhiều bước (autoregressive)** → ưu tiên kiến trúc seq2seq/direct multi-horizon thay vì lặp lại 1-bước như bản gốc
- [ ] **Rò rỉ dữ liệu (data leakage)** trong chia train/val — lỗi đã tồn tại trong repo mẫu, phải sửa triệt để trước khi tin vào bất kỳ số liệu đánh giá nào
- [ ] **Kỳ vọng sai của người dùng** về độ chính xác dự báo bão (bản chất là bài toán bất định cao) → cần truyền thông rõ bằng "cone of uncertainty" thay vì 1 đường đi khẳng định
- [ ] **Tải hệ thống tăng vọt** khi có bão lớn ảnh hưởng trực tiếp Việt Nam → cần autoscaling/kiểm thử tải trước mùa bão

# WBS CHI TIẾT — CÁC TASK NHỎ NHẤT VÀ ĐIỀU KIỆN HOÀN THÀNH

> Mục tiêu: biến roadmap thành danh sách công việc có thể giao, code, test và nghiệm thu.
> Mỗi task nên được đóng khi có đủ: **Input → Implementation → Output → Test → Definition of Done (DoD)**.

---

## 0. QUẢN LÝ PROJECT

### 0.1 Repository
- [ ] Tạo repository `typhoon-vn-forecast-system`.
- [ ] Tạo `main`, `develop`.
- [ ] Tạo branch theo feature.
- [ ] Thiết lập `.gitignore`.
- [ ] Tạo `README.md`.
- [ ] Tạo `LICENSE`.
- [ ] Tạo `CONTRIBUTING.md`.
- [ ] Thiết lập Conventional Commits.
- [ ] Thiết lập pre-commit.
- [ ] Chạy lint lần đầu.
- [ ] Commit cấu trúc ban đầu.

**DoD:** clone repo trên máy sạch và chạy được bước setup.

### 0.2 Cấu trúc thư mục
- [ ] Tạo `data/raw`.
- [ ] Tạo `data/interim`.
- [ ] Tạo `data/processed`.
- [ ] Tạo `data/external`.
- [ ] Tạo `src/ingestion`.
- [ ] Tạo `src/preprocessing`.
- [ ] Tạo `src/features`.
- [ ] Tạo `src/datasets`.
- [ ] Tạo `src/models`.
- [ ] Tạo `src/training`.
- [ ] Tạo `src/inference`.
- [ ] Tạo `src/evaluation`.
- [ ] Tạo `src/alerts`.
- [ ] Tạo `api`.
- [ ] Tạo `frontend`.
- [ ] Tạo `tests/unit`.
- [ ] Tạo `tests/integration`.
- [ ] Tạo `tests/model`.
- [ ] Tạo `configs`.
- [ ] Tạo `docs`.

**DoD:** cấu trúc thư mục thống nhất với README.

### 0.3 Environment
- [ ] Khóa Python version.
- [ ] Tạo `pyproject.toml`.
- [ ] Tạo environment.
- [ ] Cài PyTorch.
- [ ] Cài Pandas/NumPy.
- [ ] Cài Scikit-learn.
- [ ] Cài FastAPI/Uvicorn.
- [ ] Cài SQLAlchemy/Alembic.
- [ ] Cài Pytest.
- [ ] Cài MLflow.
- [ ] Cài Optuna.
- [ ] Tạo `.env.example`.
- [ ] Tạo config loader.
- [ ] Tạo Makefile/justfile.

**DoD:** `make setup` hoàn tất và `pytest` chạy được.

---

# 1. DATA INGESTION

## 1.1 CMA
- [ ] Xác định URL/source.
- [ ] Viết downloader.
- [ ] Tạo thư mục raw CMA.
- [ ] Download một file mẫu.
- [ ] Kiểm tra HTTP status.
- [ ] Retry request.
- [ ] Timeout request.
- [ ] Kiểm tra file rỗng.
- [ ] Tính checksum.
- [ ] Ghi metadata download.
- [ ] Download toàn bộ lịch sử.
- [ ] Log lỗi từng file.

**DoD:** có thể chạy một command để tải lại dữ liệu CMA.

## 1.2 CMA Parser
- [ ] Đọc file raw.
- [ ] Nhận diện storm ID.
- [ ] Parse timestamp.
- [ ] Parse latitude.
- [ ] Parse longitude.
- [ ] Parse wind.
- [ ] Parse pressure nếu có.
- [ ] Chuẩn hóa đơn vị.
- [ ] Xử lý missing.
- [ ] Xuất DataFrame chuẩn.
- [ ] Xuất Parquet.
- [ ] Viết test parser.

**DoD:** file raw → bảng chuẩn không mất các trường bắt buộc.

## 1.3 IBTrACS
- [ ] Tạo downloader.
- [ ] Cache file.
- [ ] Tạo parser.
- [ ] Chọn agency fields.
- [ ] Chuẩn hóa storm ID.
- [ ] Chuẩn hóa timestamp.
- [ ] Chuẩn hóa lat/lon.
- [ ] Chuẩn hóa wind/pressure.
- [ ] Lưu source agency.
- [ ] Validate dữ liệu.
- [ ] Export Parquet.

## 1.4 JMA
- [ ] Tạo provider.
- [ ] Downloader.
- [ ] Parser.
- [ ] Mapping schema.
- [ ] Unit conversion.
- [ ] Validation.
- [ ] Export.

## 1.5 JTWC
- [ ] Tạo provider.
- [ ] Downloader.
- [ ] Parser.
- [ ] Mapping schema.
- [ ] Unit conversion.
- [ ] Validation.
- [ ] Export.

## 1.6 NCHMF
- [ ] Xác định nguồn được phép sử dụng.
- [ ] Xác định format.
- [ ] Tạo provider interface.
- [ ] Viết parser tương ứng với nguồn thực tế.
- [ ] Parse thời điểm phát hành.
- [ ] Parse vị trí tâm bão.
- [ ] Parse cường độ.
- [ ] Parse dự báo nếu nguồn cung cấp.
- [ ] Lưu bản gốc.
- [ ] Lưu metadata.
- [ ] Test với dữ liệu mẫu.

**DoD:** adapter NCHMF có thể thay implementation mà không ảnh hưởng các module phía sau.

## 1.7 Source Merge
- [ ] Chuẩn hóa tên cột.
- [ ] Chuẩn hóa timezone.
- [ ] Chuẩn hóa đơn vị.
- [ ] Chuẩn hóa storm ID.
- [ ] Match storm giữa các nguồn.
- [ ] Match timestamp.
- [ ] Tính khoảng cách giữa các vị trí.
- [ ] Phát hiện duplicate.
- [ ] Đánh dấu conflict.
- [ ] Xác định priority source.
- [ ] Tạo master dataset.
- [ ] Lưu provenance.

## 1.8 Data Validation
- [ ] Validate latitude.
- [ ] Validate longitude.
- [ ] Validate timestamp.
- [ ] Validate wind.
- [ ] Validate pressure.
- [ ] Kiểm tra duplicate.
- [ ] Kiểm tra missing.
- [ ] Kiểm tra timestamp tăng dần.
- [ ] Kiểm tra vị trí nhảy bất thường.
- [ ] Gắn cờ suspicious thay vì âm thầm xóa.
- [ ] Sinh báo cáo quality.

---

# 2. GEOSPATIAL DATA

## 2.1 Coastline
- [ ] Chọn nguồn coastline.
- [ ] Tải dữ liệu.
- [ ] Kiểm tra CRS.
- [ ] Chuẩn hóa CRS.
- [ ] Simplify cho frontend nếu cần.
- [ ] Tạo spatial index.
- [ ] Test khoảng cách tới bờ.

## 2.2 Administrative Boundary
- [ ] Tải ranh giới tỉnh/thành.
- [ ] Kiểm tra CRS.
- [ ] Chuẩn hóa tên tỉnh.
- [ ] Tạo GeoJSON.
- [ ] Tạo spatial index.
- [ ] Test point-in-polygon.
- [ ] Test nearest province.

## 2.3 Special Locations
- [ ] Tạo danh sách các mốc cần theo dõi.
- [ ] Lưu latitude/longitude.
- [ ] Tạo ID duy nhất.
- [ ] Tạo hàm khoảng cách.
- [ ] Test kết quả.

---

# 3. PREPROCESSING

## 3.1 Pipeline
- [ ] `parse()`.
- [ ] `validate()`.
- [ ] `deduplicate()`.
- [ ] `merge()`.
- [ ] `sort()`.
- [ ] `interpolate()`.
- [ ] `feature()`.
- [ ] `export()`.

## 3.2 Missing Values
- [ ] Thống kê missing.
- [ ] Phân biệt missing thật và giá trị không hợp lệ.
- [ ] Nội suy theo từng storm.
- [ ] Không dùng 0 mặc định cho dữ liệu chưa biết.
- [ ] Gắn cờ dữ liệu được nội suy.
- [ ] Test interpolation.

## 3.3 Time Normalization
- [ ] Chuẩn hóa UTC.
- [ ] Kiểm tra duplicate timestamp.
- [ ] Sắp xếp theo thời gian.
- [ ] Kiểm tra khoảng cách thời gian.
- [ ] Resample nếu cần.
- [ ] Ghi lại quy tắc resampling.

---

# 4. FEATURE ENGINEERING

## 4.1 Position
- [ ] latitude.
- [ ] longitude.
- [ ] delta latitude.
- [ ] delta longitude.
- [ ] Position lag 1.
- [ ] Position lag 2.
- [ ] Position lag 3.

## 4.2 Motion
- [ ] Haversine distance.
- [ ] Bearing.
- [ ] Speed.
- [ ] Acceleration.
- [ ] Bearing change.
- [ ] Turning rate.
- [ ] Direction sin/cos.

## 4.3 Coast
- [ ] Distance to coastline.
- [ ] Bearing to coastline.
- [ ] Nearest coastline point.
- [ ] Distance to nearest province.

## 4.4 Time
- [ ] Hour.
- [ ] Hour sin/cos.
- [ ] Day.
- [ ] Day sin/cos.
- [ ] Month.
- [ ] Month sin/cos.
- [ ] Day of year.
- [ ] Day-of-year sin/cos.
- [ ] Season flag.

## 4.5 Intensity
- [ ] Wind.
- [ ] Pressure.
- [ ] Intensity category.
- [ ] Wind change.
- [ ] Pressure change.

## 4.6 SST
- [ ] Download SST.
- [ ] Match timestamp.
- [ ] Match grid.
- [ ] Sample SST at storm center.
- [ ] Calculate SST gradient.
- [ ] Validate missing.
- [ ] Cache extracted feature.

## 4.7 Atmospheric Features
- [ ] Load ERA5.
- [ ] Extract sea-level pressure.
- [ ] Extract 850 hPa wind.
- [ ] Extract 200 hPa wind.
- [ ] Extract humidity if available.
- [ ] Calculate wind shear.
- [ ] Validate units.
- [ ] Cache features.

## 4.8 Feature Schema
- [ ] Tạo danh sách feature chính thức.
- [ ] Đặt dtype.
- [ ] Đặt đơn vị.
- [ ] Đặt mô tả.
- [ ] Đặt nguồn.
- [ ] Đặt missing policy.
- [ ] Tạo data dictionary.

---

# 5. SCALING

- [ ] Chia train/validation/test trước khi fit scaler.
- [ ] Fit scaler chỉ trên train.
- [ ] Save scaler.
- [ ] Load scaler khi inference.
- [ ] Transform train.
- [ ] Transform validation.
- [ ] Transform test.
- [ ] Test inverse transform.
- [ ] Test không có leakage.

**DoD:** inference dùng đúng scaler của model.

---

# 6. DATASET

## 6.1 Window
- [ ] Chọn sequence length.
- [ ] Hỗ trợ cấu hình sequence length.
- [ ] Tạo sliding window.
- [ ] Tạo input tensor.
- [ ] Tạo target tensor.
- [ ] Kiểm tra boundary từng storm.

## 6.2 Horizons
- [ ] 6h.
- [ ] 12h.
- [ ] 24h.
- [ ] 48h.
- [ ] 72h.
- [ ] Kiểm tra target tồn tại.
- [ ] Bỏ sample không đủ target.

## 6.3 Split
- [ ] Split theo storm ID.
- [ ] Kiểm tra không overlap storm.
- [ ] Có tùy chọn split theo năm.
- [ ] Lưu danh sách train IDs.
- [ ] Lưu validation IDs.
- [ ] Lưu test IDs.
- [ ] Test leakage.

## 6.4 Dataset Tests
- [ ] Test shape.
- [ ] Test dtype.
- [ ] Test window.
- [ ] Test horizon.
- [ ] Test mask.
- [ ] Test storm boundary.

---

# 7. BASELINE MODELS

## 7.1 Persistence
- [ ] Implement persistence.
- [ ] Generate 6h.
- [ ] Generate 12h.
- [ ] Generate 24h.
- [ ] Generate 48h.
- [ ] Generate 72h.
- [ ] Evaluate.

## 7.2 CLIPER
- [ ] Xác định dữ liệu/phương pháp phù hợp.
- [ ] Implement baseline.
- [ ] Generate forecasts.
- [ ] Evaluate.
- [ ] Save metrics.

**DoD:** ML model phải được so sánh với baseline.

---

# 8. LSTM MODEL

## 8.1 Architecture
- [ ] Tạo BaseModel.
- [ ] Xác định input size.
- [ ] Xác định hidden size.
- [ ] Xác định number of layers.
- [ ] Xác định dropout.
- [ ] Tạo LSTM.
- [ ] Tạo output head.
- [ ] Viết forward.
- [ ] Kiểm tra tensor shape.

## 8.2 Output
- [ ] Output 6h.
- [ ] Output 12h.
- [ ] Output 24h.
- [ ] Output 48h.
- [ ] Output 72h.
- [ ] Kiểm tra lat/lon.

## 8.3 Intensity Head
- [ ] Tạo wind head.
- [ ] Tạo pressure head.
- [ ] Tạo category head nếu dữ liệu hỗ trợ.
- [ ] Kiểm tra output shape.

## 8.4 Tests
- [ ] Forward test.
- [ ] Batch-size test.
- [ ] Sequence-length test.
- [ ] Gradient test.
- [ ] Save/load test.

---

# 9. SEQ2SEQ / ATTENTION / TRANSFORMER

## 9.1 Seq2Seq
- [ ] Encoder.
- [ ] Decoder.
- [ ] Hidden state.
- [ ] Multi-step output.
- [ ] Teacher forcing nếu sử dụng.
- [ ] Test inference.

## 9.2 Attention
- [ ] Tạo attention layer.
- [ ] Tính attention score.
- [ ] Softmax.
- [ ] Context vector.
- [ ] Kết hợp output.
- [ ] Visualize attention nếu cần.

## 9.3 Transformer
- [ ] Positional encoding.
- [ ] Encoder.
- [ ] Attention.
- [ ] Feed-forward.
- [ ] Output head.
- [ ] Train baseline.
- [ ] Compare với LSTM.

**DoD:** không chọn Transformer chỉ vì phức tạp; phải chứng minh bằng metric.

---

# 10. LOSS & OPTIMIZATION

- [ ] Position loss.
- [ ] Intensity loss.
- [ ] Horizon weights.
- [ ] Haversine-based evaluation/loss nếu triển khai.
- [ ] AdamW.
- [ ] Learning-rate scheduler.
- [ ] Gradient clipping.
- [ ] Kiểm tra NaN loss.
- [ ] Log từng thành phần loss.

---

# 11. UNCERTAINTY

## 11.1 Monte Carlo Dropout
- [ ] Giữ dropout khi inference.
- [ ] Chạy nhiều sample.
- [ ] Lưu trajectories.
- [ ] Tính mean trajectory.
- [ ] Tính quantile.
- [ ] Tính radius.

## 11.2 Ensemble
- [ ] Train model seed 1.
- [ ] Train seed 2.
- [ ] Train seed 3.
- [ ] Gom predictions.
- [ ] Tính mean.
- [ ] Tính dispersion.

## 11.3 Cone
- [ ] Xác định radius theo horizon.
- [ ] Tạo polygon.
- [ ] Kiểm tra polygon hợp lệ.
- [ ] Xuất GeoJSON.
- [ ] Hiển thị trên map.

**DoD:** API trả được trajectory + uncertainty, frontend vẽ được cone.

---

# 12. TRAINING PIPELINE

- [ ] YAML config.
- [ ] Seed.
- [ ] Deterministic settings phù hợp.
- [ ] Data loader.
- [ ] Optimizer.
- [ ] Scheduler.
- [ ] Training loop.
- [ ] Validation loop.
- [ ] Early stopping.
- [ ] Gradient clipping.
- [ ] Best checkpoint.
- [ ] Last checkpoint.
- [ ] Resume training.
- [ ] Log metrics.
- [ ] Log artifacts.
- [ ] Log config.
- [ ] Log dataset version.

---

# 13. MODEL EVALUATION

## 13.1 Track Error
- [ ] Haversine prediction vs actual.
- [ ] Tính 6h.
- [ ] Tính 12h.
- [ ] Tính 24h.
- [ ] Tính 48h.
- [ ] Tính 72h.
- [ ] Mean.
- [ ] Median.
- [ ] RMSE/percentile nếu phù hợp.

## 13.2 Along/Cross Track
- [ ] Xác định reference track.
- [ ] Tính along-track error.
- [ ] Tính cross-track error.
- [ ] Kiểm tra đơn vị km.

## 13.3 Intensity
- [ ] MAE wind.
- [ ] MAE pressure.
- [ ] Accuracy/F1 category nếu có nhãn.

## 13.4 Backtest
- [ ] Chọn storms test.
- [ ] Không train bằng test storms.
- [ ] Chạy forecast từng mốc.
- [ ] So actual/predicted.
- [ ] Sinh biểu đồ.
- [ ] Tạo bảng metric.
- [ ] Phân tích case tốt.
- [ ] Phân tích case xấu.

---

# 14. HYPERPARAMETER TUNING

- [ ] Chọn search space.
- [ ] hidden size.
- [ ] layers.
- [ ] dropout.
- [ ] learning rate.
- [ ] batch size.
- [ ] sequence length.
- [ ] horizon weights.
- [ ] Chạy Optuna.
- [ ] Lưu trial.
- [ ] Chọn best config.
- [ ] Re-train best config.
- [ ] Đánh giá trên test một lần cuối.

---

# 15. MODEL REGISTRY

- [ ] Cài MLflow.
- [ ] Log model.
- [ ] Log metrics.
- [ ] Log params.
- [ ] Log dataset version.
- [ ] Tạo model registry.
- [ ] Đặt version.
- [ ] Staging.
- [ ] Production.
- [ ] Quy tắc promote.
- [ ] Rollback model.

---

# 16. INFERENCE SERVICE

## 16.1 Forecaster
- [ ] Load model một lần.
- [ ] Load scaler.
- [ ] Load feature schema.
- [ ] Validate input.
- [ ] Build features.
- [ ] Predict.
- [ ] Denormalize.
- [ ] Generate uncertainty.
- [ ] Generate impact.
- [ ] Return standardized result.

## 16.2 Rolling Forecast
- [ ] Lấy observations gần nhất.
- [ ] Tạo input window.
- [ ] Predict bước tiếp.
- [ ] Sinh multi-horizon.
- [ ] Kiểm soát autoregressive error.
- [ ] Validate output.

## 16.3 Fallback
- [ ] Phát hiện thiếu environmental feature.
- [ ] Dùng fallback hợp lệ.
- [ ] Gắn cờ `fallback_used`.
- [ ] Log fallback.

---

# 17. FASTAPI

- [ ] Tạo FastAPI app.
- [ ] `/health`.
- [ ] `/version`.
- [ ] `/forecast`.
- [ ] `/typhoons/active`.
- [ ] `/typhoons/{id}/track`.
- [ ] `/typhoons/{id}/impact`.
- [ ] Pydantic request schemas.
- [ ] Pydantic response schemas.
- [ ] Error handler.
- [ ] Logging.
- [ ] OpenAPI.
- [ ] API key nếu public.
- [ ] Rate limit nếu public.

**DoD:** Swagger UI gọi được forecast end-to-end.

---

# 18. DATABASE / POSTGIS

## 18.1 Tables
- [ ] `typhoons`.
- [ ] `observations`.
- [ ] `forecasts`.
- [ ] `forecast_points`.
- [ ] `alerts`.
- [ ] `model_versions`.
- [ ] `users`.
- [ ] `subscriptions`.

## 18.2 Migration
- [ ] Alembic init.
- [ ] Initial migration.
- [ ] Index.
- [ ] Spatial index.
- [ ] Foreign keys.
- [ ] Constraints.

## 18.3 Audit
- [ ] Lưu thời điểm dự báo.
- [ ] Lưu model version.
- [ ] Lưu input version.
- [ ] Lưu output.
- [ ] Lưu forecast run ID.

---

# 19. REAL-TIME WORKER

- [ ] Tạo worker.
- [ ] Scheduler.
- [ ] Fetch latest source.
- [ ] Validate new records.
- [ ] Detect new observation.
- [ ] Trigger inference.
- [ ] Save forecast.
- [ ] Update cache.
- [ ] Retry failure.
- [ ] Log worker status.

---

# 20. REDIS

- [ ] Cache active typhoons.
- [ ] Cache latest forecast.
- [ ] Cache API response.
- [ ] TTL.
- [ ] Cache invalidation.
- [ ] Test cache hit/miss.

---

# 21. FRONTEND

## 21.1 Setup
- [ ] Tạo React/Next.js.
- [ ] Router.
- [ ] API client.
- [ ] State management.
- [ ] CSS/theme.
- [ ] Environment config.

## 21.2 Map
- [ ] Leaflet.
- [ ] Vietnam boundary.
- [ ] Coastline.
- [ ] Storm marker.
- [ ] Historical track.
- [ ] Forecast track.
- [ ] Cone.
- [ ] Province layer.

## 21.3 Dashboard
- [ ] Active storm list.
- [ ] Storm status.
- [ ] Map.
- [ ] Legend.
- [ ] Last update.
- [ ] Data source.

## 21.4 Storm Detail
- [ ] Storm name.
- [ ] Position.
- [ ] Wind.
- [ ] Pressure.
- [ ] Direction.
- [ ] Speed.
- [ ] Forecast table.
- [ ] Timeline.

## 21.5 Province Impact
- [ ] Select province.
- [ ] Calculate distance.
- [ ] Display ETA.
- [ ] Display impact level.
- [ ] Display uncertainty.
- [ ] Show source/time.

## 21.6 Mobile
- [ ] Responsive map.
- [ ] Responsive cards.
- [ ] Responsive timeline.
- [ ] Test mobile width.
- [ ] Test tablet.

---

# 22. ALERT ENGINE

- [ ] Thiết kế alert rule.
- [ ] Distance threshold.
- [ ] Time threshold.
- [ ] Severity.
- [ ] Subscription area.
- [ ] Generate message.
- [ ] Add source.
- [ ] Add issue time.
- [ ] Add disclaimer.
- [ ] Send channel.
- [ ] Retry.
- [ ] Throttle.
- [ ] Alert history.

---

# 23. TESTING

## 23.1 Unit
- [ ] Haversine.
- [ ] Bearing.
- [ ] Position.
- [ ] Feature builder.
- [ ] Scaler.
- [ ] Dataset.
- [ ] Model.
- [ ] Cone.
- [ ] Alert rules.

## 23.2 Integration
- [ ] Raw → clean.
- [ ] Clean → feature.
- [ ] Feature → dataset.
- [ ] Dataset → train.
- [ ] Train → model.
- [ ] Model → inference.
- [ ] Inference → API.
- [ ] API → frontend.

## 23.3 Edge cases
- [ ] Missing observation.
- [ ] Missing SST.
- [ ] Missing wind shear.
- [ ] Sudden turn.
- [ ] Near coastline.
- [ ] Weakening storm.
- [ ] Invalid coordinate.
- [ ] Duplicate observation.
- [ ] Multiple active storms.

## 23.4 Load
- [ ] API concurrent requests.
- [ ] Database load.
- [ ] Cache load.
- [ ] Worker retry.
- [ ] Traffic spike scenario.

---

# 24. DOCKER

- [ ] Backend Dockerfile.
- [ ] Worker Dockerfile.
- [ ] Frontend Dockerfile.
- [ ] Training image nếu cần.
- [ ] Postgres service.
- [ ] Redis service.
- [ ] Network.
- [ ] Volumes.
- [ ] Environment.
- [ ] Health checks.
- [ ] Production compose.

---

# 25. CI/CD

- [ ] GitHub Actions.
- [ ] Install dependencies.
- [ ] Lint.
- [ ] Unit test.
- [ ] Integration test.
- [ ] Build backend.
- [ ] Build frontend.
- [ ] Build Docker image.
- [ ] Security/basic dependency check nếu phù hợp.
- [ ] Deploy staging.
- [ ] Model evaluation gate.
- [ ] Production deployment.
- [ ] Rollback.

---

# 26. MONITORING

## System
- [ ] API uptime.
- [ ] API latency.
- [ ] Error rate.
- [ ] Worker status.
- [ ] Database status.
- [ ] Redis status.
- [ ] CPU.
- [ ] RAM.
- [ ] Disk.

## Data
- [ ] Last update timestamp.
- [ ] Missing rate.
- [ ] Schema drift.
- [ ] Source failure.
- [ ] Data delay.

## Model
- [ ] Input distribution.
- [ ] Feature drift.
- [ ] Prediction distribution.
- [ ] Error after actual track arrives.
- [ ] Model version.

---

# 27. DOCUMENTATION

- [ ] Architecture.
- [ ] Data source.
- [ ] Data dictionary.
- [ ] Feature engineering.
- [ ] Dataset.
- [ ] Model.
- [ ] Training.
- [ ] Evaluation.
- [ ] API.
- [ ] Database.
- [ ] Frontend.
- [ ] Deployment.
- [ ] Runbook.
- [ ] User guide.
- [ ] Disclaimer.

---

# 28. DEMO / NGHIỆM THU

## Demo 1 — Dữ liệu
- [ ] Chọn một cơn bão.
- [ ] Hiển thị lịch sử.
- [ ] Chứng minh data pipeline.

## Demo 2 — Model
- [ ] Load model.
- [ ] Nhập observation.
- [ ] Sinh 6/12/24/48/72h.
- [ ] Hiển thị metric.

## Demo 3 — Bản đồ
- [ ] Actual track.
- [ ] Forecast track.
- [ ] Cone.
- [ ] Province impact.

## Demo 4 — API
- [ ] Swagger.
- [ ] POST forecast.
- [ ] Response.
- [ ] Error handling.

## Demo 5 — Real-time
- [ ] Mock observation mới.
- [ ] Worker nhận dữ liệu.
- [ ] Trigger inference.
- [ ] Dashboard cập nhật.

## Demo 6 — Alert
- [ ] Tạo subscription.
- [ ] Kích hoạt rule.
- [ ] Sinh cảnh báo.
- [ ] Kiểm tra throttle.

---

# 29. DEFINITION OF DONE TOÀN PROJECT

Project chỉ được xem là hoàn chỉnh khi:

- [ ] Có dữ liệu lịch sử có provenance.
- [ ] Có pipeline ingestion tự động.
- [ ] Có validation và cleaning.
- [ ] Có feature engineering.
- [ ] Không có data leakage.
- [ ] Có train/validation/test độc lập.
- [ ] Có baseline.
- [ ] Có ít nhất một model ML hoạt động.
- [ ] Có multi-horizon forecast.
- [ ] Có metric theo km.
- [ ] Có backtest.
- [ ] Có uncertainty/cone.
- [ ] Có model version.
- [ ] Có inference service.
- [ ] Có FastAPI.
- [ ] Có PostgreSQL/PostGIS.
- [ ] Có dashboard bản đồ.
- [ ] Có actual + forecast track.
- [ ] Có vùng ảnh hưởng.
- [ ] Có cảnh báo nếu triển khai.
- [ ] Có unit/integration/model tests.
- [ ] Có Docker.
- [ ] Có CI/CD cơ bản.
- [ ] Có logging/monitoring cơ bản.
- [ ] Có tài liệu cài đặt.
- [ ] Có tài liệu kiến trúc.
- [ ] Có báo cáo đánh giá.
- [ ] Có disclaimer rõ ràng.

---

# 30. THỨ TỰ THỰC HIỆN KHUYẾN NGHỊ

Không làm Frontend trước Model.

Thứ tự:

```text
01. Repository
        ↓
02. Environment
        ↓
03. CMA/IBTrACS data
        ↓
04. Cleaning
        ↓
05. Geospatial
        ↓
06. Feature engineering
        ↓
07. Dataset
        ↓
08. Train/Val/Test
        ↓
09. Persistence baseline
        ↓
10. LSTM baseline
        ↓
11. Multi-horizon
        ↓
12. Evaluation
        ↓
13. Attention/Transformer
        ↓
14. Uncertainty
        ↓
15. Model Registry
        ↓
16. Inference
        ↓
17. FastAPI
        ↓
18. PostgreSQL/PostGIS
        ↓
19. Frontend
        ↓
20. Alert
        ↓
21. Worker/Realtime
        ↓
22. Docker
        ↓
23. CI/CD
        ↓
24. Monitoring
        ↓
25. Documentation
        ↓
26. Demo + nghiệm thu
```

---

# 31. MỐI QUAN HỆ DEPENDENCY

```text
DATA
  │
  ▼
PREPROCESSING
  │
  ▼
FEATURE
  │
  ▼
DATASET
  │
  ├──────────────► BASELINE
  │
  ▼
LSTM
  │
  ▼
EVALUATION
  │
  ├──────────────► ATTENTION
  │                     │
  │                     ▼
  │                 TRANSFORMER
  │                     │
  ▼                     ▼
UNCERTAINTY ◄──────── MODEL SELECTION
  │
  ▼
INFERENCE
  │
  ▼
API
  │
  ├────────────► DATABASE
  │
  ▼
FRONTEND
  │
  ▼
ALERT
```

> **Nguyên tắc:** Không được đánh giá model bằng test set rồi quay lại tune model trên chính test set. Test set cuối cùng phải được giữ độc lập.
