# Typhoon Path Prediction

> Mô hình dự đoán đường đi bão sử dụng LSTM

![comparison plot](./result/animation_20230010.gif)

## Mục lục

- [Tổng quan](#tổng-quan)
- [Cài đặt](#cài-đặt)
- [Chuẩn bị dữ liệu](#chuẩn-bị-dữ-liệu)
- [Lựa chọn đặc trưng](#lựa-chọn-đặc-trưng)
- [Huấn luyện mô hình](#huấn-luyện-mô-hình)
- [Dự đoán](#dự-đoán)
- [Giấy phép](#giấy-phép)

---

## Tổng quan

Dự án này cung cấp một quy trình hoàn chỉnh để dự đoán đường đi của bão bằng mô hình dựa trên LSTM. Mô hình dự đoán đường đi của bão bằng cách sử dụng dữ liệu của 4 điểm thời gian trước để dự báo điểm thời gian tiếp theo. Quy trình bao gồm chuẩn bị dữ liệu, trích xuất đặc trưng, huấn luyện mô hình, dự đoán và trực quan hóa kết quả.

---

## Cài đặt

### Yêu cầu:
- Python 3.x
- Trình quản lý gói `pip`

### Các bước:

1. **Clone repository này:**
   ```bash
   git clone https://github.com/VietManh05/typhoon-track-vietnam.git
   ```

2. **Di chuyển vào thư mục repository:**
   ```bash
   cd typhoon-track-vietnam
   ```

3. **Cài đặt các dependency:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Chuẩn bị dữ liệu

Chúng tôi sử dụng [CMA Tropical Cyclone Best Track Dataset](https://tcdata.typhoon.org.cn/en/zjljsjj.html).

Để làm sạch và chuẩn bị dữ liệu, chạy lệnh:
   ```bash
   python3 data_clean.py
   ```

**Thay đổi:**

- Cột `END`: Ghi lại trạng thái của xoáy thuận tại thời điểm hiện tại:
    - 0: Chưa kết thúc
    - 1: Tan rã
    - 2: Di chuyển ra ngoài khu vực trách nhiệm của Ủy ban Bão Tây Thái Bình Dương
    - 3: Hợp nhất
    - 4: Ổn định gần như đứng yên
- Cột `distance_km` và `bearing`: Đại diện cho khoảng cách Haversine và góc bearing từ điểm thời gian trước đến điểm thời gian hiện tại, giúp cung cấp thêm thông tin không gian về chuyển động của xoáy thuận.

---

## Lựa chọn đặc trưng

Chúng tôi cải thiện biểu diễn đặc trưng của mô hình bằng các kỹ thuật sau:

- **Temporal Features**: Chuyển đổi cột `Time` thành biểu diễn tuần hoàn (giờ, ngày, tháng, năm) bằng phép biến đổi sin và cos để nắm bắt các mẫu theo chu kỳ theo thời gian.

- **Bearing**: Góc `bearing` cũng được biến đổi bằng sin và cos để nắm bắt tốt hơn các mối quan hệ góc.

- **Categorical Features**:
    - `I` (Intensity) và `END` (Status) được mã hóa one-hot để cho phép mô hình phân biệt giữa các danh mục khác nhau.

- **Normalization**:
    - Các cột số còn lại được chuẩn hóa bằng min-max scaling để đồng bộ dữ liệu và cải thiện hiệu quả huấn luyện mô hình.

---

## Huấn luyện mô hình

Để huấn luyện mô hình:
   ```bash
   python3 train.py
   ```


**Chi tiết huấn luyện**:

- **Loss function**: `SmoothL1Loss` (Huber Loss), được lựa chọn vì khả năng mạnh đối với outliers, đồng thời cân bằng giữa hàm mất mát L1 và L2.

- **Optimizer**: `AdamW`, kết hợp lợi ích của Adam (tốc độ học thích ứng) với weight decay để ngăn overfitting và cải thiện khả năng tổng quát hóa.

- **Data split**:
    - 90% dữ liệu được sử dụng cho huấn luyện.
    - 10% được dành cho validation.

- Mô hình tốt nhất được lưu tự động dựa trên validation loss.

---

## Dự đoán

Để thực hiện dự đoán:
   ```bash
   python3 predict.py
   ```

- Bạn có thể chỉ định `typhoonID` để chạy dự đoán.
- Mô hình sử dụng dữ liệu của 4 điểm thời gian trước để dự đoán dữ liệu bão ở điểm thời gian tiếp theo.
- Sau khi dự đoán, một GIF so sánh dữ liệu thực tế và dữ liệu dự đoán sẽ được tạo ra.

---

## Giấy phép

Dự án này được cấp phép theo **MIT License**. Xem chi tiết trong tệp [LICENSE](./LICENSE).
