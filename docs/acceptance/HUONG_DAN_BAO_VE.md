# Hướng dẫn trình bày và bảo vệ đồ án

**Đề tài:** Xây dựng hệ thống hỗ trợ gợi ý đường đi của cơn bão Việt Nam
(môn Trí tuệ nhân tạo). Mọi số liệu dưới đây lấy từ
[`docs/report/README.md`](../report/README.md) và
[`docs/acceptance/README.md`](README.md); chạy lại được bằng lệnh ghi trong báo cáo.

## 1. Một câu mô tả

Hệ thống dự báo vị trí tâm bão tại +6/12/24/48/72 giờ cho bão có thể ảnh hưởng
Việt Nam, kèm **vùng bất định đã hiệu chỉnh** và **danh sách các cơn bão lịch sử
giống nhất** làm căn cứ cho gợi ý. Đây là bài toán **dự báo chuỗi thời gian
nhiều mốc**, không phải bài toán tìm đường (bão không "chọn" đường đi).

## 2. Kịch bản demo 5 phút

Website: <https://baoviet2026.pages.dev>

1. **Bản đồ trực tiếp** (30 giây): bão đang hoạt động lấy từ bản tin JMA, có nhãn
   nguồn và dòng cảnh báo "không thay thế bản tin NCHMF".
2. **Bấm "Dự báo lại"** (1 phút): 20 cơn bão thật 2021–2024 ảnh hưởng Việt Nam. Mô
   hình **chưa thấy** các bão này khi huấn luyện. Nói rõ đây là dự báo lại, không
   phải bão đang hoạt động.
3. **Chọn YAGI 2024** (2 phút): đường xanh là quỹ đạo đã đi, vàng là LSTM, hồng là
   gợi ý k-NN, tím là quỹ đạo thực tế sau thời điểm dự báo. Mở khung
   "Gợi ý theo bão tương tự" để đọc tên 5 cơn bão (WUKONG 2000, DAMREY 2005, …) và
   bảng sai số. Thừa nhận thẳng: LSTM dự báo bão rẽ lên tây bắc, thực tế đi thẳng
   vào miền Bắc; đây là ca khó (xem mục 5).
4. **Vùng bất định** (30 giây): nón không phải số minh họa; bán kính lấy phân vị
   80% sai số trên tập validation, độ phủ thực tế trên test là 82–86%.
5. **Chuyển sang slide kết quả** (1 phút): bảng ở mục 3.

## 3. Số liệu chính (test 2021–2024, 84 bão, 714 cửa sổ)

| Phương pháp | 6h | 12h | 24h | 48h | 72h (km) |
|---|---:|---:|---:|---:|---:|
| Persistence (mốc so sánh) | 31 | 68 | 155 | 390 | 676 |
| k-NN analog | 32 | 64 | 133 | 290 | 462 |
| LSTM (đang phục vụ) | 33 | 65 | 133 | 289 | 464 |
| Transformer | 33 | 64 | 133 | 293 | 468 |

* Học từ dữ liệu giảm sai số 72 h khoảng **200 km (~30%)** so với persistence, có ý
  nghĩa thống kê (bootstrap theo cơn bão, KTC 95% không chứa 0).
* LSTM, Transformer, k-NN và gradient boosting **không khác nhau có ý nghĩa**.
* Thêm **dòng dẫn đường khí quyển** (NCEP, 11 đặc trưng) và ensemble LSTM +
  Transformer, chọn cấu hình trên validation: tốt hơn mô hình đang phục vụ
  **35 km tại 72 h, KTC 95% [−62, −9]** (trung bình các mốc 179 so với 197 km).
  Chưa đưa vào website vì cần dữ liệu khí quyển gần thời gian thực.

## 4. Chạy lại trên máy

```powershell
python -m pip install -e ".[api,train,ingestion,dev]"   # Python 3.11
python -m pytest -q                            # 177 đạt, 4 bỏ qua
python -m uvicorn typhoon_vn.api.app:app       # mở http://127.0.0.1:8000
```

Gói mô hình đã huấn luyện không nằm trong git. Khi chưa có, API ở chế độ phát
triển tự dùng mốc persistence. Muốn phục vụ bằng LSTM và k-NN thì tạo lại bằng
các lệnh "Tái lập kết quả" trong báo cáo, rồi đặt
`$env:MODEL_ARTIFACT` (thư mục bundle) và `$env:ANALOG_ARTIFACT` (file `.npz`)
trước khi chạy API.

Docker: `docker build -f infra/docker/Dockerfile -t typhoon-vn .` rồi mount hai
artefact ở chế độ chỉ đọc và đặt hai biến môi trường trên trỏ tới đó.

## 5. Câu hỏi thường gặp và cách trả lời trung thực

* **"Sao không dùng A\*/tìm đường?"** Bão là hiện tượng vật lý, không có tác nhân
  chọn đường. "Gợi ý" ở đây là gợi ý quỹ đạo kèm độ bất định và các bão tương tự.
* **"Có rò rỉ dữ liệu không?"** Chia theo năm, giữ nguyên cả cơn bão (train 1980–2016,
  validation 2017–2020, test 2021–2024); scaler chỉ fit trên train; mọi lựa chọn
  trên validation, test chạy một lần; thư viện k-NN phục vụ loại bỏ bão test.
* **"Sao học sâu không hơn k-NN?"** Chỉ có ~7.800 cửa sổ huấn luyện và đặc trưng chỉ
  từ quỹ đạo; hướng đi của bão chủ yếu do dòng dẫn đường khí quyển. Khi thêm đặc
  trưng đó mới có cải thiện có ý nghĩa.
* **"YAGI sai nhiều?"** Đúng. Tại 72 h, LSTM sai 541 km và Transformer 678 km;
  gradient boosting (407 km) và k-NN (419 km) gần đúng hơn; kể cả khi thêm dòng
  dẫn đường, các mô hình vẫn sai khoảng 620–670 km. Lưới 2,5° và
  đặc trưng tóm tắt chưa đủ nhận ra áp cao cận nhiệt mạnh; hướng tiếp theo là ERA5
  0,25° và đặc trưng dạng ảnh.
* **"Website có dự báo bão đang hoạt động không?"** Chưa chạy mô hình trên bão trực
  tiếp: JMA không cung cấp thời điểm cho các điểm quá khứ, nên đầu vào sẽ phải
  đoán. Mô hình được trình diễn trên bão đã qua (dự báo lại).
* **"Có thể dùng để cảnh báo không?"** Không. Mọi giao diện ghi "không thay thế bản
  tin NCHMF". Kênh gửi cảnh báo qua webhook đã viết và kiểm thử nhưng **tắt mặc
  định**, chỉ bật khi có phê duyệt nghiệp vụ.
* **"CI đâu?"** GitHub Actions chạy mỗi lần push lên `main`: lint, 177 test Python
  (có PostGIS thật), 42 test Node, build frontend và đối chiếu dashboard; đang xanh.
