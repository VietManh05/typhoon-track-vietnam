# Evidence: Gate G21 — Frontend và Bản Đồ (T21-001 đến T21-039, S10-S12)

- **Thời gian thực hiện**: 2026-09-19
- **Mục tiêu**: Hoàn thiện toàn bộ Frontend Dashboard cho hệ thống Typhoon VN theo đúng lộ trình WBS nhóm 21.
- **Thành phần thực hiện**:
  - `viz/frontend/`: Toàn bộ ứng dụng React 18 + TypeScript + Vite + Leaflet + Lucide Icons.
  - `viz/frontend/public/data/vietnam_provinces.geojson`: 63 tỉnh thành trích xuất từ GADM v4.1.
  - `viz/frontend/public/data/vietnam_islands.json`: Tọa độ và vùng biển chủ quyền Quần đảo Hoàng Sa và Quần đảo Trường Sa.
  - `src/typhoon_vn/dashboard/`: Bản phân phối static được đồng bộ từ `viz/frontend/dist/`.
  - `src/typhoon_vn/api/app.py`: Tích hợp CORSMiddleware và static mount cho `/`, `/assets`, `/data`, `/favicon.svg`.
  - `tests/test_frontend_build.py`: Bộ kiểm thử tích hợp FastAPI phục vụ Dashboard.
  - `docs/frontend.md`: Tài liệu kỹ thuật chi tiết.

## Các Task Đã Hoàn Thành (Theo WBS G21 & Supplemental Tasks)

| Task ID | Nội dung | Kết quả kiểm chứng |
|---------|----------|-------------------|
| **T21-001** | Tạo React/Next.js | React 18 + TypeScript + Vite khởi tạo tại `viz/frontend` |
| **T21-002** | Router | SPA routing với State-driven screen switching |
| **T21-003** | API client | `src/services/api.ts` hỗ trợ gọi FastAPI + Fallback Mock |
| **T21-004** | State management | Central state management tại `App.tsx` |
| **T21-005** | CSS/theme | `src/index.css` với Radar Palette, Glassmorphism, Dark/Light mode |
| **T21-006** | Environment config | `vite.config.ts` dev reverse proxy + multi-mode serving |
| **T21-007** | Leaflet | `src/components/Map/TyphoonMap.tsx` tương tác mượt mà |
| **T21-008** | Vietnam boundary | Biên giới quốc gia Việt Nam hiển thị nổi bật |
| **T21-009** | Coastline | Đường bờ biển sắc nét tương phản cao |
| **T21-010** | Storm marker | Custom SVG Marker tâm bão xoay động kèm hiệu ứng sóng lan |
| **T21-011** | Historical track | Đường nét liền màu lục (`#10b981`) kèm quan trắc thực tế |
| **T21-012** | Forecast track | Đường nét đứt màu hổ phách (`#f59e0b`) các mốc +6h đến +72h |
| **T21-013** | Cone | Nón bất định bán trong suốt GeoJSON polygon |
| **T21-014** | Province layer | Lớp 63 tỉnh thành Việt Nam với hover tooltip & click highlight |
| **T21-015** | Active storm list | Tab bar chuyển đổi nhanh các cơn bão đang hoạt động |
| **T21-016** | Storm status | Badge trạng thái (Active, Category, Wind speed) |
| **T21-017** | Map | Layout bản đồ trung tâm Biển Đông tỷ lệ toàn màn hình |
| **T21-018** | Legend | Bảng chú giải nổi `MapLegend.tsx` giải thích màu sắc, nét vẽ |
| **T21-019** | Last update | Hiển thị thời gian quan trắc gần nhất theo giờ UTC và VN |
| **T21-020** | Data source | Badges nguồn dữ liệu (NCHMF, JMA, JTWC, AI Model version) |
| **T21-021** | Storm name | Tên bão song ngữ (Bão Yagi, Bão số 3, Bão số 6...) |
| **T21-022** | Position | Tọa độ tâm bão chính xác (Vĩ độ/Kinh độ) |
| **T21-023** | Wind | Sức gió theo km/h, m/s và Cấp gió Beaufort |
| **T21-024** | Pressure | Khí áp tâm bão (hPa) |
| **T21-025** | Direction | Góc phương vị la bàn (Bearing °) và hướng la bàn (WNW, NW...) |
| **T21-026** | Speed | Tốc độ di chuyển về phía trước (km/h) |
| **T21-027** | Forecast table | Bảng dự báo đa thời đoạn `ForecastTable.tsx` (+6h...+72h) |
| **T21-028** | Timeline | Thanh trượt `TimelinePlayer.tsx` tua mốc quan trắc & tự động Play |
| **T21-029** | Select province | Ô tìm kiếm và chọn nhanh 63 tỉnh/thành phố |
| **T21-030** | Calculate distance | Tính khoảng cách Geodesic Haversine (km) tức thì |
| **T21-031** | Display ETA | Dự báo thời gian tiếp cận gần nhất (giờ và ngày) |
| **T21-032** | Display impact level | 5 cấp độ rủi ro (Rất nguy hiểm, Mạnh, Trung bình, Thấp, An toàn) |
| **T21-033** | Display uncertainty | Cảnh báo nằm trong hoặc ngoài nón xác suất |
| **T21-034** | Show source/time | Ghi chú minh bạch phương pháp luận hình học |
| **T21-035** | Responsive map | Co giãn linh hoạt theo tỷ lệ khung nhìn |
| **T21-036** | Responsive cards | Grid responsive 7-5 trên Desktop, Stack cột trên Mobile |
| **T21-037** | Responsive timeline | Thanh trượt touch-friendly co giãn theo bề rộng màn hình |
| **T21-038** | Test mobile width | Kiểm tra tương thích viewport mobile 360x800 |
| **T21-039** | Test tablet | Kiểm tra tương thích viewport tablet 768x1024 |
| **S10** | So sánh dự báo | Lớp overlay so sánh quỹ đạo mô hình AI vs NCHMF/JTWC |
| **S11** | Giao diện Việt/Anh | Nút chuyển đổi song ngữ Tiếng Việt 🇻🇳 (mặc định) & English 🇬🇧 |
| **S12** | Chú giải cấp bão | Bảng phân loại cấp bão chuẩn NCHMF (Áp thấp nhiệt đới -> Siêu bão) |

## Bằng Chứng Kiểm Thử Tự Động (Command Evidence)

### 1. Build Production Frontend
```bash
$ npm run build
> typhoon-vn-frontend@1.0.0 build
> tsc && vite build
vite v5.4.21 building for production...
dist/index.html                   1.56 kB
dist/assets/index-DxL4NG0r.css    4.21 kB
dist/assets/index--q0cYYuY.js   366.74 kB
✓ built in 4.81s
Exit code: 0
```

### 2. Kiểm Thử Pytest Phục Vụ Dashboard Qua FastAPI
```bash
$ .venv\Scripts\pytest tests/test_frontend_build.py --basetemp=.pytest-frontend -v
tests/test_frontend_build.py::test_dashboard_static_files_served_by_fastapi PASSED [100%]
Exit code: 0
```

### 3. Kiểm Thử Toàn Bộ Tuyến Đường HTTP Server Trực Tiếp
```bash
$ .venv\Scripts\python scripts/verify_dashboard_http.py
ROUTE: /                                   STATUS: 200 LEN: 1617     CT: text/html; charset=utf-8
ROUTE: /favicon.svg                        STATUS: 200 LEN: 1030     CT: image/svg+xml
ROUTE: /data/vietnam_provinces.geojson     STATUS: 200 LEN: 906365   CT: application/octet-stream
ROUTE: /data/vietnam_islands.json          STATUS: 200 LEN: 906      CT: application/json
ROUTE: /health                             STATUS: 200 LEN: 43       CT: application/json
ROUTE: /version                            STATUS: 200 LEN: 108      CT: application/json
ROUTE: /typhoons/active                    STATUS: 200 LEN: 165      CT: application/json
ASSET: /assets/index--q0cYYuY.js           STATUS: 200 LEN: 367816
ASSET: /assets/index-DxL4NG0r.css          STATUS: 200 LEN: 4208

ALL VERIFICATION CHECKS PASSED: True
Exit code: 0
```
