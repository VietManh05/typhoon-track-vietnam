# Chạy và deploy Typhoon VN

## Trạng thái xác minh

20/09/2026: 209 test Python đạt; 1 test PostGIS cần POSTGIS_TEST_URL nên chưa chạy. Frontend build và cấu hình Compose được kiểm tra. Docker Engine chưa hoạt động trên máy kiểm tra nên chưa xác minh build/chạy container hoặc VPS thực tế.

Thời tiết địa phương cần ACCUWEATHER_API_KEY. Bản đồ Windy Map Forecast là tích hợp tùy chọn qua VITE_WINDY_MAP_API_KEY; khi thiếu key hoặc SDK lỗi, giao diện tự dùng Leaflet/OpenStreetMap. Thủy văn/Hải văn chưa có nguồn dữ liệu. Baseline và dữ liệu demo không phải dự báo đã được kiểm định.

## Chạy Windows

Cần Python 3.11 và Node.js (CI dùng Node 20). Từ thư mục project:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[api,train,dev]"
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn typhoon_vn.api.app:create_app --factory --host 127.0.0.1 --port 8000
```

Trong .env đặt API_KEY ngẫu nhiên, APP_ENV=development, ALLOW_BASELINE=true. Nếu dùng Windy, đặt thêm `VITE_WINDY_MAP_API_KEY` bằng Map Forecast key (không phải Point Forecast key). Key này được nhúng vào JavaScript trình duyệt; Testing key chỉ dùng cho phát triển. Terminal khác:

```powershell
cd viz/frontend
npm ci
npm run dev -- --host 127.0.0.1
```

Mở http://127.0.0.1:5173. Muốn cập nhật giao diện backend cổng 8000, từ gốc
project chỉ cần chạy build. Vite đã ghi trực tiếp vào
`src/typhoon_vn/dashboard`; không copy từ `viz/frontend/dist` vì đó có thể là
bundle cũ:

```powershell
npm --prefix viz/frontend run build
```

Deploy bản Cloudflare Pages `baoviet2026` bằng cổng kiểm tra output bắt buộc:

```powershell
npm --prefix viz/frontend run deploy:pages
```

Lệnh này build, xác nhận bundle có giao diện Ollama mới rồi mới deploy đúng thư
mục `src/typhoon_vn/dashboard`. Secret `OLLAMA_API_KEY` phải được đặt bằng
Wrangler/Cloudflare, không ghi vào source hoặc biến `VITE_*`.

## Docker preview, chưa cần model

Bật Docker Desktop với Linux containers; docker info phải thành công. Copy configs/deploy.env.example thành .env.preview và đổi API_KEY. Các trường model/Postgres không dùng ở preview.

```powershell
Copy-Item configs/deploy.env.example .env.preview
docker compose --env-file .env.preview -f docker-compose.preview.yml config --quiet
docker compose --env-file .env.preview -f docker-compose.preview.yml up -d --build
docker compose --env-file .env.preview -f docker-compose.preview.yml ps
curl.exe -f http://127.0.0.1:8080/ready
```

Mở http://127.0.0.1:8080. Preview dùng baseline và SQLite trong volume riêng, chỉ bind localhost. Nginx phục vụ frontend và chuyển tiếp API cùng origin.

## Production trên VPS Linux

Cần Docker Engine + Compose plugin, source project, bundle model đã kiểm định và domain nếu dùng HTTPS. Không chuyển .venv/node_modules/.env cá nhân vào image.

```bash
cp configs/deploy.env.example .env.production
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

Đổi API_KEY và POSTGRES_PASSWORD thành hai giá trị ngẫu nhiên khác nhau. MODEL_HOST_PATH là đường dẫn tuyệt đối tới thư mục bundle chứa manifest.json và các file checksum do pipeline xuất; không phải file .pth riêng lẻ. Điền ACCUWEATHER_API_KEY nếu có. Production bắt buộc ALLOW_BASELINE=false và có model.

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml config --quiet
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build postgres redis api frontend
docker compose --env-file .env.production -f docker-compose.prod.yml ps
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=100 api frontend
curl -f http://127.0.0.1:8080/health
curl -f http://127.0.0.1:8080/ready
curl -f http://127.0.0.1:8080/version
```

API tự chạy Alembic khi khởi tạo Store. Lần đầu chạy một API instance trước khi tăng số instance để tránh migration đồng thời. Thiếu model thì API cố ý không khởi động production.

Trỏ DNS domain về VPS và đặt reverse proxy HTTPS trên host tới 127.0.0.1:8080. Ví dụ Caddyfile (thay domain, cài và chạy Caddy theo tài liệu chính thức; mở 80/443):

```caddyfile
weather.example.com {
    reverse_proxy 127.0.0.1:8080
}
```

PostgreSQL/Redis không mở port host; 8000/8080/9090 chỉ bind localhost. Endpoint bảo vệ dùng X-API-Key từ công cụ quản trị; không nhúng API_KEY trong JavaScript public.

## Worker

Worker xử lý snapshot, chưa tự cào website. Cung cấp observations.json trong SNAPSHOT_HOST_PATH, là JSON array theo ObservationBatch trong /docs (storm_id, name, observations; mỗi observation có timestamp UTC, lat, lon, wind_ms, pressure_hpa, intensity, source).

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml --profile worker up -d --build worker
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=100 worker
```

Worker đọc snapshot mỗi 30 phút; nguồn bên ngoài phải cập nhật file. Worker không gửi email ra ngoài.

## Kiểm tra và cập nhật

```bash
python -m pytest -q
npm --prefix viz/frontend run build
```

POSTGIS_TEST_URL phải trỏ database kiểm thử riêng. Trước deploy mới: sao lưu PostgreSQL bằng pg_dump, giữ bundle model và ghi lại commit/image tag. Dùng image tag theo commit. Rollback bằng TYPHOON_API_IMAGE/TYPHOON_FRONTEND_IMAGE/TYPHOON_WORKER_IMAGE tag cũ rồi compose up -d --no-build. Rollback image không tự rollback database; kiểm tra tương thích migration. Không dùng down -v vì xóa volume dữ liệu.

Tham khảo: https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/ và https://docs.docker.com/compose/how-tos/startup-order/
