# Phiếu nghiệm thu UAT — bản demo Typhoon VN

Phạm vi đề nghị: **giao diện bản đồ, thời tiết địa phương, trợ lý giải thích và chế độ xem dữ liệu bão mẫu** trên <https://baoviet2026.pages.dev/>. Phiếu này không nghiệm thu dự báo/cảnh báo bão vận hành.

## Bằng chứng kỹ thuật đã tự động kiểm tra

- `demo-release-smoke-2026-09-23.json`: 23/23 route, asset, nguồn thời tiết và trạng thái dữ liệu đạt.
- `demo-ui-smoke-2026-09-23.json`: 10/10 kiểm tra đạt, gồm badge DEMO/chuông cảnh báo/đăng nhập và bố cục ở 320, 390, 430, 768, 1024, 1440 px; menu lớp bản đồ đóng/mở trên mobile không đè lên tìm kiếm.
- Backend: 254 test đạt, 1 test PostGIS bị bỏ qua khi không có `POSTGIS_TEST_URL`. Frontend: 19 test đạt; lint và build đạt.
- `/ready` của Pages trả 503 JSON vì chưa có backend dự báo vận hành. Đây là kết quả đúng cho bản demo.

## Bước người nhận cần xác nhận

| Mục | Thao tác và kết quả mong đợi | Xác nhận |
| --- | --- | --- |
| Bản đồ | Mở trang trên điện thoại và desktop; phóng/thu, đổi lớp nền, tìm địa điểm. Control không chồng nhau và bản đồ phản hồi. | ☐ |
| Thời tiết | Chọn Đà Nẵng hoặc địa điểm khác; thấy nhiệt độ, thời điểm, nhà cung cấp và trạng thái dữ liệu. | ☐ |
| Bão mẫu | Khi chưa có feed, giao diện nói rõ chưa kết nối; chỉ khi chọn “Xem demo” mới thấy dữ liệu bão mẫu. | ☐ |
| AI | Gửi câu hỏi giải thích thông thường; câu trả lời không tự nhận là bản tin dự báo/cảnh báo chính thức. Nếu dịch vụ ngoài tạm lỗi, giao diện báo lỗi rõ. | ☐ |
| Giới hạn | Người nhận hiểu trang này không phát cảnh báo và không thay bản tin NCHMF; đăng nhập không khả dụng trên Pages. | ☐ |
| Bàn giao nguồn | Mở ZIP, kiểm tra `HANDOVER-MANIFEST.json`; lưu SHA-256 toàn ZIP và URL triển khai cùng phiếu. | ☐ |

Người nghiệm thu: ____________________  Ngày: __________  Kết quả demo: ☐ Đạt  ☐ Cần sửa

Nếu cần nghiệm thu **vận hành**, phải mở phiếu riêng với bằng chứng dữ liệu bão hợp lệ, model được đánh giá trên dữ liệu thật, backend/PostGIS/worker chạy ở môi trường đích, người nhận cảnh báo và quy trình ứng phó. Không chuyển các ô này sang “đạt” bằng dữ liệu mẫu hoặc bằng bản Pages hiện tại.
