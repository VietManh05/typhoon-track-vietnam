# Biên bản rà soát và nghiệm thu Typhoon VN — 27/09/2026

**Kết luận:** Đạt cho phạm vi xem bản tin bão JMA và thời tiết trực tuyến ở bản Pages. **Chưa đạt nghiệm thu vận hành hệ thống dự báo riêng và gửi cảnh báo.** Typhoon VN là công cụ hỗ trợ tham khảo, không phải kênh cảnh báo chính thức tại Việt Nam.

## Phạm vi khách hàng có thể xem ngay

- URL: <https://baoviet2026.pages.dev/>. Bản triển khai được đối chiếu: <https://4c5930bf.baoviet2026.pages.dev/>.
- Bão đang hoạt động và quỹ đạo lấy từ JMA RSMC Tokyo, có thời gian quan trắc, liên kết nguồn và cảnh báo theo dõi NCHMF. Nguồn có thể thay đổi hoặc gián đoạn; khi bản tin hết hạn, ứng dụng bỏ trạng thái LIVE.
- Thời tiết địa phương lấy từ Open-Meteo. Trợ lý AI có endpoint được cấu hình nhưng không phải nguồn quan trắc hoặc cảnh báo.
- Nút chuông mở được hộp thoại giải thích dịch vụ gửi cảnh báo chưa khả dụng và dẫn tới NCHMF. Hệ thống hiện không nhận đăng ký gửi cảnh báo.

## Kết quả rà soát mã và bằng chứng

Rà soát các nhánh mã chính và kiểm tra tự động trên toàn bộ `src`, `tests`, Pages Functions và frontend:

| Nhánh mã | Kết luận review |
| --- | --- |
| Ingestion, làm sạch và đặc trưng | Có checksum nguồn và tách train/validation/test theo bão/năm. Snapshot IBTrACS 2015–2025 có 8.679 hàng đầu vào, 5.220 hàng sạch; 3.459 hàng nằm ngoài miền dự báo Việt Nam của dự án; không có hàng nào mang tọa độ WGS84 sai. Đây là giới hạn phạm vi dữ liệu, không phải lỗi tọa độ nguồn. Cần kiểm toán độ phủ miền trước khi duyệt mô hình. |
| Huấn luyện, suy luận và đánh giá | Đã sửa dự báo quanh vị trí quan trắc cuối, thêm mốc chuyển động gần nhất và siết kiểm tra bundle. Ứng viên vẫn chưa qua mốc +6 giờ và độ bất định chưa được hiệu chuẩn. |
| FastAPI, xác thực, lưu trữ | Đọc JMA được mở công khai có rate limit; route dữ liệu nội bộ còn xác thực. CORS được thu hẹp. Wheel và SQLite khởi động được; PostGIS trên hạ tầng thật chưa được kiểm tra trong lần này. |
| Cảnh báo và worker | Chỉ có bản nháp, fake transport và xử lý snapshot; không có người nhận hay kênh gửi thật. Đây là thiếu chức năng cốt lõi cho nghiệm thu cảnh báo. |
| Pages Functions và giao diện | Bridge dùng HTTPS và secret phía máy chủ, kiểm tra phiên bản/revision/độ mới trước khi hiện dự báo riêng. Giao diện giữ trạng thái LIVE/DEMO theo nguồn bão, nút cảnh báo hoạt động và nói rõ dịch vụ gửi chưa bật. |
| Triển khai, CI và vận hành | CI có kiểm tra mã, bộ test, wheel và container; máy rà soát hiện không chạy Docker/PostGIS. Cần lặp lại các cổng này trên đích sản xuất và lưu bằng chứng. |

| Phạm vi | Kết quả rà soát đến 27/09/2026 |
| --- | --- |
| Backend, dữ liệu, mô hình, API và vận hành | `pytest`: **263 passed, 1 skipped**, 3 cảnh báo thư viện; ca PostGIS thật bị bỏ qua do chưa có `POSTGIS_TEST_URL`. |
| Python quality | `flake8 src tests`: 0 lỗi; `isort --check-only src tests` và `black --check src tests`: đạt. `pip check`: không có dependency hỏng. |
| Frontend và Pages Functions | 25/25 ca kiểm tra qua; TypeScript lint và build Vite đạt; kiểm tra output Pages đạt. `npm audit --omit=dev --audit-level=high`: 0 lỗ hổng được báo tại thời điểm kiểm tra. |
| Gói phát hành Python | Wheel xây dựng được; cài ngoài thư mục repo và khởi động Store kèm migrations đạt. |
| Site công khai | Trang chủ, `/health`, `/typhoons/active`, quỹ đạo `TC2632` và ba endpoint thời tiết trả HTTP 200 khi quan sát ngày 26/09/2026 lúc khoảng 16:55 UTC. Kiểm tra lại ngày 27/09: `/health` HTTP 200, `/ready` và `/subscriptions` HTTP 503 đúng theo trạng thái chưa đủ điều kiện. `/health` báo `stormFeed:true`, `modelForecast:false`, `alertDelivery:false`. |
| Giao diện thật | Chrome headless xác nhận huy hiệu `BÃO LIVE`, nút chuông mở hộp thoại NCHMF; ở 390 px, vùng bấm 44×44 px và không bị lớp khác che. |

Các thay đổi quan trọng trong lần rà soát: mở đọc JMA công khai có giới hạn tần suất nhưng giữ dữ liệu lưu trữ/mô hình sau xác thực; thay CORS `*` bằng danh sách origin cấu hình; đồng bộ `/health` và `/ready` với trạng thái backend/mô hình/cảnh báo; xác thực phiên bản và độ mới của dữ liệu backend ở Pages; sửa mô hình thử nghiệm học dịch chuyển quanh vị trí bão và kiểm tra bundle theo horizon; cập nhật ca hồi quy và mô tả công khai để không nhận là dự báo Deep Learning khi chưa có mô hình được duyệt.

Lệnh tái hiện chính: `python -m pytest -q`, `python -m flake8 src tests`, `python -m isort --check-only src tests`, `python -m black --check src tests`, `npm --prefix viz/frontend test`, `npm --prefix viz/frontend run lint`, `npm --prefix viz/frontend run build`, `python scripts/verify_wheel.py <wheel>`, `python scripts/verify_live_ui.py`. Kết quả phụ thuộc dữ liệu nguồn và trạng thái site tại thời điểm chạy.

## Các điều kiện chưa đạt trước khi ký nghiệm thu vận hành

1. **Backend sản xuất:** Chưa có URL HTTPS và quyền triển khai FastAPI. Máy rà soát không có Docker daemon đang chạy, không có `.env.production` hoặc thư mục mô hình `checkpoints/promoted`; chưa chạy PostGIS/Redis/worker tại đích. Pages đang báo `/ready` HTTP 503 và `/auth/capabilities.available:false`.
2. **Mô hình dự báo riêng:** Ứng viên IBTrACS gần nhất chưa vượt mốc persistence ở +6 giờ trên tập đã dùng trong quá trình nghiên cứu: 37,46 km so với 36,65 km (280 dự báo, 49 bão trong tập kiểm tra). +12 đến +72 giờ tốt hơn mốc này nhưng chưa đủ điều kiện. Tập đó đã được xem trong các lần chỉnh mô hình, vì vậy cần một tập kiểm tra độc lập mới trước khi tuyên bố đạt; bán kính bất định hiện là heuristic minh họa, chưa có bằng chứng hiệu chuẩn độ phủ. Không có mô hình nào được tự động đưa vào sản xuất.
3. **Gửi cảnh báo:** Backend mới lưu bản nháp; chưa có kênh gửi thật, địa chỉ/người nhận được chấp thuận, xác nhận đăng ký, lịch chạy và bằng chứng gửi/nhận/thử lại. `/subscriptions` và `/ready` trên Pages trả HTTP 503 có chủ đích. Không được mô tả nút chuông là dịch vụ thông báo đang hoạt động.
4. **Vận hành và an toàn:** Cần cấu hình bí mật ở máy chủ/Cloudflare, kiểm tra backup–restore, giám sát và rollback trên hạ tầng đích, kiểm soát lạm dụng AI và API ở tầng biên, cùng chấp thuận nguồn dữ liệu và nội dung gửi cho khách. Các giới hạn tần suất trong bộ nhớ một tiến trình không thay thế kiểm soát phân tán khi triển khai nhiều replica.

## Tiêu chí đóng các chặn

- Có URL HTTPS backend và môi trường PostGIS/Redis; chạy migrations, worker, `/health`, `/ready`, `/version`, metrics và PostGIS integration trên chính đích triển khai. Ghi phiên bản triển khai và kết quả rollback.
- Dùng dữ liệu có provenance và bộ holdout mới chưa dùng để điều chỉnh mô hình; báo MAE/median/p90 theo từng horizon, so với persistence và mốc nghiệp vụ do khách phê duyệt; hiệu chuẩn và kiểm tra độ phủ vùng bất định; chỉ sau đó mới ký duyệt một bundle cụ thể.
- Chọn kênh gửi, danh sách người nhận thử nghiệm được phép, cơ chế xác nhận/hủy đăng ký, lưu kết quả gửi và thử lại; kiểm tra end-to-end trên người nhận thử nghiệm trước khi bật `delivery: active`.
- Cấu hình các biến bí mật Pages (`TYPHOON_BACKEND_URL`, API key, phiên bản và revision mô hình được duyệt), kiểm tra `/ready` HTTP 200, `modelForecast:true`, `alertDelivery:true`, đăng ký và nhận cảnh báo trên site công khai; lưu bằng chứng tại thời điểm nghiệm thu.

Nguồn dữ liệu cần ghi công: [JMA và điều kiện sử dụng](https://www.jma.go.jp/jma/en/copyright.html), [NOAA IBTrACS v4r01](https://www.ncei.noaa.gov/products/international-best-track-archive). Hướng dẫn ràng buộc biến và secrets Pages: [Cloudflare Pages Functions bindings](https://developers.cloudflare.com/pages/functions/bindings/).
