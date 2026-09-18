# Kế hoạch chi tiết Typhoon VN

Ngày lập lại: 2026-09-18. Phạm vi: toàn roadmap; phiên hiện tại chỉ lập lại kế hoạch.
Ảnh đính kèm là ngữ cảnh giải thích skill, không phải yêu cầu cài thêm skill hoặc khởi động lại ứng dụng.
**635 task WBS + 24 task bổ sung = 659 task thực thi**, **28 tiêu chí nghiệm thu**, kèm **14 task ưu tiên** là lát cắt thực thi của backlog, không cộng trùng phạm vi.

## Cách thực hiện từng task

1. Đọc task_plan.md → next_tasks.md → đúng task card.
2. Kiểm tra dependency và code có sẵn; kiểm chứng/sửa phần thiếu, không viết lại mặc định.
3. Một task in_progress tại một thời điểm; cập nhật Next Step.
4. Lưu command, exit code, expected/actual và evidence; chỉ đánh complete khi đạt DoD.
5. Thiếu dữ liệu/tài khoản thì giữ pending, ghi blocker và làm task độc lập. Không cần xin lại quyền cho sửa chữa đã được ủy quyền.
6. Cập nhật findings/progress/task_plan sau mỗi task; không có bằng chứng thì chưa hoàn thành.

## File điều phối

- [14 việc làm ngay](next_tasks.md)
- [Quyết định và cổng nghiệm thu](execution_policy.md)
- [Đối chiếu toàn bộ checkbox](traceability.md)
- [Bổ sung yêu cầu chỉ có ở phần tổng quan](supplemental_tasks.md)
- [Nghiệm thu toàn dự án](acceptance.md)

## WBS

- **G00 — Nền tảng repository và môi trường**: [45 mục](wbs-00.md); phụ thuộc: Không.
- **G01 — Ingestion và nguồn gốc dữ liệu**: [83 mục](wbs-01.md); phụ thuộc: G00.
- **G02 — Dữ liệu không gian**: [19 mục](wbs-02.md); phụ thuộc: G00.
- **G03 — Làm sạch và thời gian**: [20 mục](wbs-03.md); phụ thuộc: G01.
- **G04 — Feature engineering**: [54 mục](wbs-04.md); phụ thuộc: G02, G03.
- **G05 — Scaling không rò rỉ**: [9 mục](wbs-05.md); phụ thuộc: G04, G06.
- **G06 — Dataset và phân chia tập**: [26 mục](wbs-06.md); phụ thuộc: G03, G04.
- **G07 — Baseline cổ điển**: [12 mục](wbs-07.md); phụ thuộc: G06.
- **G08 — LSTM cơ sở**: [24 mục](wbs-08.md); phụ thuộc: G05, G06.
- **G09 — Seq2Seq, attention và Transformer**: [19 mục](wbs-09.md); phụ thuộc: G12, G13.
- **G10 — Loss và tối ưu**: [9 mục](wbs-10.md); phụ thuộc: G08.
- **G11 — Bất định và cone**: [17 mục](wbs-11.md); phụ thuộc: G13, G14.
- **G12 — Training tái lập**: [17 mục](wbs-12.md); phụ thuộc: G05, G06, G08, G10.
- **G13 — Đánh giá và backtest**: [24 mục](wbs-13.md); phụ thuộc: G07, G12.
- **G14 — Tuning và kiểm định theo mùa**: [13 mục](wbs-14.md); phụ thuộc: G09, G13.
- **G15 — Model registry và promotion**: [11 mục](wbs-15.md); phụ thuộc: G11, G14.
- **G16 — Dịch vụ inference**: [20 mục](wbs-16.md); phụ thuộc: G15.
- **G17 — FastAPI**: [14 mục](wbs-17.md); phụ thuộc: G16, G18.
- **G18 — Database, PostGIS và migration**: [19 mục](wbs-18.md); phụ thuộc: G00, G02.
- **G19 — Worker thời gian thực**: [10 mục](wbs-19.md); phụ thuộc: G01, G17, G20.
- **G20 — Redis và invalidation**: [6 mục](wbs-20.md); phụ thuộc: G17.
- **G21 — Frontend và bản đồ**: [39 mục](wbs-21.md); phụ thuộc: G02, G17.
- **G22 — Alert engine và kênh tích hợp**: [13 mục](wbs-22.md); phụ thuộc: G19, G21.
- **G23 — Kiểm thử xuyên hệ thống**: [31 mục](wbs-23.md); phụ thuộc: G19, G21, G22.
- **G24 — Container và cấu hình production**: [11 mục](wbs-24.md); phụ thuộc: G23.
- **G25 — CI/CD và phát hành**: [13 mục](wbs-25.md); phụ thuộc: G24.
- **G26 — Monitoring, drift và backup**: [19 mục](wbs-26.md); phụ thuộc: G24.
- **G27 — Tài liệu và hướng dẫn**: [15 mục](wbs-27.md); phụ thuộc: G26.
- **G28 — Demo và nghiệm thu**: [23 mục](wbs-28.md); phụ thuộc: G23, G25, G26, G27.
- **G29 — Definition of Done toàn dự án**: [28 mục](acceptance.md); phụ thuộc: G28.
