# Kiểm toán toàn bộ Typhoon VN

Ngày kiểm tra: 2026-09-26 (Asia/Saigon)

## Kết luận điều hành

Repository có các thành phần ingestion, preprocessing, bốn kiến trúc neural,
baselines, training/checkpoint, bundle, inference, API, dashboard, weather,
alerts và worker. Kiểm tra local xác nhận các kiểm thử hiện có chạy được trên
Python 3.11.9 và frontend build được. Điều đó xác nhận hợp đồng phần mềm và
đường chạy demo; không xác nhận chất lượng dự báo bão ngoài thực tế.

**Chưa đạt trạng thái vận hành dự báo/cảnh báo bão.** Pages hiện có weather
trực tiếp nhưng không có live storm feed, model bundle được promote, đăng nhập
hay gửi alert. PostGIS thật và hạ tầng production chưa được kiểm thử trong lượt
này.

## Kiểm tra đã chạy

| Phạm vi | Kết quả ngày 2026-09-26 |
| --- | --- |
| Backend: `.venv\Scripts\python.exe -m pytest -q` | 255 passed, 1 skipped, 3 warnings, 40.02s |
| PostGIS integration | Skipped vì thiếu `POSTGIS_TEST_URL` |
| Python Black | Pass, 139 files unchanged |
| Python isort | Pass |
| Python flake8 | Pass |
| Frontend `npm test` | 19 passed |
| Frontend `npm run lint` | Pass (`tsc --noEmit`) |
| Frontend `npm run build` | Pass, 2088 modules; sinh dashboard vào `src/typhoon_vn/dashboard` |
| Preview Compose parse | Pass với `configs/deploy.env.example`; không chạy container |
| Cloudflare Pages `/health` | HTTP response JSON báo `status: ok`, environment `cloudflare-pages`; `weather=true`, `ai=true`, `stormFeed=false`, `alertDelivery=false` |
| Pages `/ready` | JSON `not_ready`: forecasting backend, live storm feed và alert delivery chưa kết nối |
| Pages `/typhoons/active` | JSON `typhoons: []`, `feedAvailable: false` |
| Pages weather bundle Đà Nẵng | JSON hiện tại từ Open-Meteo trả thành công, có provenance/time/location |
| Pages `/auth/capabilities` | `available:false`, authentication cần Python backend |
| Pages `/alerts` | `ALERTS_UNAVAILABLE`, lịch sử alert cần Python backend |

Lần gọi pytest đầu tiên bằng `pytest` mặc định đã dùng Python 3.14 hệ thống và
collection lỗi vì thiếu extras. Chạy đúng interpreter Python 3.11.9 của `.venv`
cho kết quả 255 pass. Dùng interpreter của `.venv` như lệnh ở trên.

## Tình trạng theo phân hệ

### Dữ liệu và ingestion

- Có provider cho IBTrACS, CMA, JMA, JTWC, dữ liệu địa lý và trường môi trường;
  có xử lý provenance/checksum và kiểm thử lỗi HTTP bằng fixture.
- `data/raw` hiện chỉ có placeholder trong checkout đã kiểm tra; chưa chạy tải
  IBTrACS mới trong lượt này và chưa xác minh giấy phép/quyền sử dụng tập dữ
  liệu cho phát hành.
- Snapshot NCHMF trong reports là dữ liệu tham khảo cũ; không chứng minh feed
  NCHMF đang hoạt động hôm nay. Pages hiện cấp weather từ Open-Meteo.

### Features, dataset và model

- Có `LSTMTrackForecaster`, `Seq2SeqLSTMTrackForecaster`,
  `AttentionLSTMTrackForecaster`, `TransformerTrackForecaster`,
  `PersistenceForecaster` và `CLIPERForecaster` dạng damped-persistence proxy.
- Bộ backend hiện pass, trong đó có test training/export/reload cho các kiến
  trúc. Đây là smoke/contract coverage trên fixture; không phải đánh giá skill.
- Có checkpoint cũ trong `checkpoints/`, nhưng không thấy bundle tại
  `checkpoints/promoted/manifest.json`. Checkpoint cũ không được xem như model
  production đã xác nhận.
- Evaluation artifact trong `reports/evaluation` ghi dataset
  `synthetic-functional-v1`, split contract-only hoặc scope synthetic. Không
  dùng metric đó để tuyên bố độ chính xác bão thật.
- Chưa chạy training fresh trên IBTrACS, chưa có test cuối độc lập theo storm,
  chưa so sánh với GFS/ECMWF track và chưa chứng minh uncertainty coverage được
  hiệu chỉnh trên dữ liệu held-out thật.
- Bundle schema hiện là phiên bản 2; báo cáo khắc phục trước đó yêu cầu đánh
  giá/train lại model artifact cũ trước khi promotion.

### Training, evaluation và inference

- Training CLI/config/checkpoint-resume/export bundle được kiểm thử. Config
  `configs/ibtracs_smoke.yaml` chỉ là một epoch CPU smoke, không phải benchmark.
- `run.py` resolve checkpoint trong `output_dir / config.checkpoint.dir`; việc
  truyền cấu hình cần kiểm tra qua từng lệnh chạy thực tế nếu thay config.
- API/inference có baseline fallback ở cấu hình local, provenance và cache.
  Production config yêu cầu bundle và tắt baseline; hiện Pages không kết nối
  Python forecaster.
- Chưa chạy end-to-end forecast bằng promoted bundle thật trong môi trường
  deploy.

### API, thời tiết, AI và giao diện

- API, auth validation, weather, cache và response contract có unit/integration
  tests. Frontend tests kiểm tra credential states, lỗi feed, Ollama proxy,
  weather retry và Windy map runtime.
- Pages weather endpoint đang hoạt động read-only; mẫu response ở
  `/api/weather/bundle?location_id=da-nang` có dữ liệu Open-Meteo tại thời điểm
  kiểm tra.
- AI capability được Pages health quảng cáo là có; frontend tests xác nhận
  proxy/error handling, nhưng lượt này không gửi prompt tới Ollama thật và
  không xác nhận model AI đang sẵn sàng.
- Pages hiện không có live storm feed, không có authentication backend và không
  gửi alert. Dashboard phải tiếp tục thể hiện rõ demo/offline/unavailable.
- TypeScript/build/test đạt local. Responsive UI đã được kiểm tra thủ công ở
  các viewport desktop, tablet, mobile dọc và ngang thấp trong lượt sửa trước;
  đây không thay thế QA thiết bị thật/screen reader.

### Lưu trữ, worker, alert và triển khai

- Có migrations, database abstraction, Redis cache, snapshot worker, alert
  engine/channels, Compose, Dockerfiles và monitoring configuration; test suite
  có unit coverage cho các hợp đồng chính.
- Compose preview chỉ được parse cấu hình; Docker containers, Redis, PostGIS,
  Prometheus scrape, worker restart/replay, gửi nhận alert và backup/restore
  thật chưa được chạy.
- Không có `POSTGIS_TEST_URL` nên PostGIS gate chưa được chứng minh. `/ready`
  của Pages cố ý báo `not_ready`; đây không phải backend readiness.
- Chưa kiểm tra DNS/TLS/VPS hay backend production trong lượt này.

## Lỗi và nội dung được xử lý trong lượt kiểm toán

- Khôi phục `docs/data-ingestion.md` từ `HEAD`; README có link đến tệp này nhưng
  working tree trước lượt kiểm tra đánh dấu tệp bị xóa.
- Bổ sung `docs/model-card.md` và `docs/handover-slides.md`; hai tệp được test
  Phase 7 yêu cầu nhưng trước đó không tồn tại. Nội dung nêu rõ trạng thái
  synthetic/demo và cổng production còn thiếu.
- Sửa frontend responsive trong [App.tsx](../viz/frontend/src/App.tsx),
  [MapLegend.tsx](../viz/frontend/src/components/Map/MapLegend.tsx) và
  [fullscreen-map.css](../viz/frontend/src/styles/fullscreen-map.css).
- Không xóa/reset các thay đổi khác trong working tree; repository trước lượt
  này đã có nhiều tệp modified/untracked và artifacts sinh sẵn.

## Việc còn lại để đạt vận hành

1. Cấu hình data source được cấp quyền, tải IBTrACS, ghi checksum/version, rà
   chất lượng dữ liệu và chạy training thật có log/artifact tái lập.
2. So sánh bốn model trên split theo storm/năm, cùng preprocessing và forecast
   horizons; giữ test độc lập chưa dùng để chọn model.
3. Đánh giá MAE km ở +6/+12/+24/+48/+72 giờ so với persistence và forecast NWP
   khớp issue/valid time; calibrate uncertainty trên validation và báo cáo
   coverage trên test.
4. Tạo/promote bundle schema 2 chỉ sau review metrics; kiểm tra serving bằng
   bundle đó và provenance/hash.
5. Chạy PostGIS/Redis/API/worker/Prometheus trong môi trường deploy; kiểm tra
   migrations trên backup, `/ready`, retry/restart, backup/restore, alert
   recipient thật có phê duyệt và rollback.
6. Hoàn thiện nguồn xác thực backend cho frontend, kiểm tra HTTPS/TLS, deploy
   một commit/tag sạch và thực hiện UAT trên URL đích.

**Quyết định hiện tại:** đạt mức code/demo local có test; chưa đạt nghiệm thu
dự báo bão hoặc cảnh báo vận hành. Không phải hệ thống cảnh báo chính thức.
