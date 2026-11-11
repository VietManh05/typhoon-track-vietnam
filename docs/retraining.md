# Tự huấn luyện ứng viên đường đi bão

Nguồn huấn luyện miễn phí là [NOAA IBTrACS v04r01, tập Western Pacific](https://www.ncei.noaa.gov/products/international-best-track-archive). Đây là chuỗi vị trí **đã quan trắc** theo thời gian. Dữ liệu dự báo JMA trên trang web dùng để hiển thị tình hình hiện tại, không được đưa vào nhãn huấn luyện như thể là vị trí bão đã xảy ra.

Chạy từ thư mục gốc bằng Python 3.11 đã cài `.[train,ingestion]`:

```powershell
rtk proxy .venv\Scripts\python.exe scripts/auto_retrain_ibtracs.py --config configs/ibtracs_candidate.yaml
```

Lệnh tải bản IBTrACS mới, ghi checksum và nguồn, chuyển thành các phân vùng quan trắc, huấn luyện trên các mùa đã hoàn tất đến hết năm trước, rồi lưu ứng viên trong `data/processed/retraining/<id>/`. Chạy lại với cùng nguồn, cấu hình và khoảng năm sẽ bỏ qua. Dùng `--use-local-source` khi muốn chạy trên CSV đã tải. `--end-year` cho phép chọn mốc năm cố định để tái lập kết quả.

`configs/ibtracs_candidate.yaml` giới hạn 12 epoch và dừng sớm theo validation; `configs/ibtracs_smoke.yaml` chỉ có một epoch để kiểm tra luồng. `training-summary.json`, `bundle/manifest.json`, `split-manifest.json` và `heldout-evaluation.json` ghi nguồn, tập train/validation/test, sai số theo hạn và so sánh với ngoại suy chuyển động. Ứng viên có sai số trung bình cao hơn baseline ở bất kỳ hạn nào được đánh dấu `rejected_baseline`; lệnh trả mã 2 để job theo lịch báo lỗi nhưng vẫn giữ artifact đánh giá. Script không xuất bản lên Cloudflare Pages, không tự promote vào production và không coi bán kính sai số minh họa là độ tin cậy đã hiệu chỉnh.

Để chạy theo lịch, dùng GitHub Actions `retrain.yml` trên nhánh mặc định; workflow chạy mỗi năm ngày 15 tháng 1 hoặc chạy thủ công. Máy chạy cần đủ thời gian và dung lượng cho CSV IBTrACS, Parquet và PyTorch. Nếu chạy trên Windows riêng, đặt Task Scheduler gọi đúng lệnh trên với `Start in` là thư mục dự án và tài khoản có quyền ghi `data/processed/retraining`.

Trước khi đưa ứng viên lên bản live cần đo sai số đường đi từng hạn dự báo trên tập bão/năm độc lập, so với persistence và dự báo nghiệp vụ, kiểm tra hiệu chỉnh vùng bất định và được người vận hành duyệt theo [model card](model-card.md). Cloudflare Pages hiện chỉ lấy bản tin JMA để hiển thị; Pages không chạy pipeline Python/PyTorch này.

## Kết quả chạy cục bộ ngày 26-09-2026

Với bản CSV checksum `08544ff3530de9df3dc77c235d24a431dc4aea1daa548120029733d5ea4483cc`, cấu hình 12 epoch và dữ liệu 2015–2024, pipeline chọn 238 cơn bão, giữ 37 cơn cho tập test. Trên 371 cửa sổ dự báo hoàn chỉnh, sai số trung bình của ứng viên ở hạn 6 giờ là khoảng **13.335 km** so với **28 km** của persistence. Ở cả năm hạn 6–72 giờ, ứng viên thua persistence nên kết quả được đánh dấu `rejected_baseline` và không được dùng cho trang live. Đây là bằng chứng huấn luyện tự động chạy được, đồng thời cho thấy kiến trúc/đầu ra hiện tại cần sửa và đánh giá lại trước khi cân nhắc sử dụng.
