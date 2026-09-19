# Typhoon VN Dashboard & Frontend Documentation (Gate G21)

Hệ thống giao diện trực quan hóa, theo dõi quỹ đạo và đánh giá rủi ro thiên tai bão nhiệt đới tại Biển Đông và lãnh thổ Việt Nam.

## 1. Kiến Trúc Kỹ Thuật

- **Vị trí mã nguồn**: `viz/frontend/`
- **Thư mục phân phối (Production build)**: `viz/frontend/dist/` và đồng bộ vào `src/typhoon_vn/dashboard/` để FastAPI phục vụ trực tiếp.
- **Tech Stack**:
  - **Framework**: React 18 + TypeScript 5
  - **Bundler**: Vite 5
  - **Bản đồ GIS**: Leaflet 1.9 với tile layers Dark Matter (CartoDB), OpenStreetMap, ESRI World Imagery
  - **Hệ thống biểu tượng**: Lucide React
  - **Thiết kế**: Vanilla CSS với CSS Variables & Glassmorphism chuẩn khí tượng vũ trụ (Dark mode & Light mode)
  - **Đa ngôn ngữ**: Hệ thống từ điển song ngữ Tiếng Việt 🇻🇳 (mặc định) và English 🇬🇧

## 2. Các Thành Phần Chính

### 2.1. Bản Đồ Tương Tác & Chủ Quyền Lãnh Thổ (`src/components/Map/TyphoonMap.tsx`)
- Tọa độ trung tâm: Vùng Biển Đông và lãnh thổ Việt Nam (`[16.5, 110.0]`, zoom 6).
- Lớp 63 tỉnh/thành phố (`/data/vietnam_provinces.geojson`): Trích xuất từ GADM v4.1, có hover tooltip và hỗ trợ bấm chọn để phân tích rủi ro.
- Lớp khẳng định chủ quyền biển đảo (`/data/vietnam_islands.json`):
  - **Quần đảo Hoàng Sa** (Thuộc TP. Đà Nẵng, Việt Nam)
  - **Quần đảo Trường Sa** (Thuộc Tỉnh Khánh Hòa, Việt Nam)
  - Đảo Bạch Long Vĩ (TP. Hải Phòng) & Đảo Phú Quốc (Tỉnh Kiên Giang)
- Quỹ đạo thực tế (Solid green polyline) kèm các điểm quan trắc (Fix markers) hiển thị thông số khí áp, sức gió, cấp bão khi bấm xem popup.
- Điểm tâm bão hiện tại với hiệu ứng xoay radar xoáy bão và vòng sóng lan tỏa (Pulsing ring effect).
- Quỹ đạo dự báo (Dashed amber polyline) nối các mốc +6h, +12h, +24h, +48h, +72h.
- Vùng nón bất định (Cone of Uncertainty polygon) bán trong suốt với viền gradient.
- Chế độ so sánh dự báo chính thức (S10): Toggle so sánh mô hình AI vs NCHMF / JTWC.

### 2.2. Bảng Điều Khiển & Thông Số Bão (`src/components/StormOverviewCard.tsx`)
- Tên bão, tên quốc tế, số hiệu bão Việt Nam (ví dụ: Bão số 3 Yagi).
- Cấp bão chuẩn NCHMF / WMO:
  - **TD**: Áp thấp nhiệt đới (< 17.2 m/s, Cấp 6-7)
  - **TS**: Bão nhiệt đới (17.2 - 24.4 m/s, Cấp 8-9)
  - **STS**: Bão mạnh (24.5 - 32.6 m/s, Cấp 10-11)
  - **TY**: Bão rất mạnh (32.7 - 41.4 m/s, Cấp 12-13)
  - **STY**: Bão cuồng phong (41.5 - 50.9 m/s, Cấp 14-15)
  - **SUPERTY**: Siêu bão (≥ 51.0 m/s, ≥ Cấp 16)
- Sức gió lớn nhất (km/h, m/s, Cấp Beaufort), Khí áp trung tâm (hPa), Tọa độ tâm bão, Tốc độ và hướng di chuyển (Bearing & Cardinal direction).
- Cảnh báo bão & Model version provenance.

### 2.3. Dòng Thời Gian Tua Quỹ Đạo (`src/components/TimelinePlayer.tsx`)
- Thanh trượt dòng thời gian hỗ trợ:
  - Tua lại quá trình bão di chuyển trong quá khứ qua từng mốc quan trắc.
  - Dự phóng chuyển động trong tương lai tới 72 giờ.
  - Nút Play/Pause tự động phát chuyển động bão.
  - Nút lùi/tiến từng bước (Step backward / forward).

### 2.4. Phân Tích Rủi Ro 63 Tỉnh Thành (`src/components/ProvinceImpactPanel.tsx`)
- Tìm kiếm nhanh 63 tỉnh/thành hoặc click trực tiếp trên bản đồ.
- Tự động tính toán khoảng cách Geodesic Haversine từ tâm bão tới tỉnh (km).
- Khoảng cách tiếp cận gần nhất trong dự báo và ETA (thời gian tiếp cận gần nhất).
- Phân loại cấp độ ảnh hưởng: Rất nguy hiểm, Ảnh hưởng mạnh, Ảnh hưởng trung bình, Ảnh hưởng xa, Ngoài vùng nguy cấp.
- Hiển thị ghi chú khoa học minh bạch: *"Khoảng cách hình học tâm bão & nón dự báo không phản ánh toàn bộ vùng mưa lũ diện rộng và gió giật thực tế."*

### 2.5. Bảng Dự Báo Đa Thời Đoạn (`src/components/ForecastTable.tsx`)
- Bảng tổng hợp các mốc +6h, +12h, +24h, +48h, +72h với giờ Việt Nam (GMT+7), tọa độ dự báo, cấp bão, sức gió và bán kính nón sai số (km).

### 2.6. Cảnh Báo Bản Quyền & Nghiệm Thu A29 (`src/components/DisclaimerBanner.tsx`)
- Thanh thông báo cố định: *"CẢNH BÁO PHÁP LÝ & KHOA HỌC: Hệ thống hỗ trợ ra quyết định thử nghiệm; không thay thế bản tin cảnh báo chính thức của Trung tâm Dự báo Khí tượng Thủy văn Quốc gia (NCHMF)."*

## 3. Cách Vận Hành

### Chạy Môi Trường Phát Triển (Dev Mode)
```bash
cd viz/frontend
npm install
npm run dev
```
Truy cập: `http://localhost:5173/` (Vite dev server tự động proxy các API call `/typhoons`, `/forecast`, `/health` sang backend FastAPI).

### Build Production & Đồng Bộ Dashboard
```bash
cd viz/frontend
npm run build
python -c "import shutil; shutil.rmtree('src/typhoon_vn/dashboard', ignore_errors=True); shutil.copytree('viz/frontend/dist', 'src/typhoon_vn/dashboard')"
```

### Chạy Toàn Bộ Hệ Thống Với FastAPI
```bash
.venv\Scripts\python -m uvicorn typhoon_vn.api.app:app --host 127.0.0.1 --port 8000
```
Mở trình duyệt truy cập ngay root URL: `http://localhost:8000/`.

## 4. Kiểm Thử Hệ Thống (Automated Verification)
Chạy test tích hợp FastAPI phục vụ Dashboard:
```bash
.venv\Scripts\pytest tests/test_frontend_build.py --basetemp=.pytest-frontend -v
```
Kiểm tra trực tiếp các route HTTP:
```bash
.venv\Scripts\python scripts/verify_dashboard_http.py
```
