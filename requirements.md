# BUỔI THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC MQTT

## 1. Mục tiêu buổi thực hành

Sau buổi thực hành, sinh viên cần:

- Hiểu cách một ứng dụng Python kết nối tới MQTT broker.
- Biết cách publish và subscribe dữ liệu qua topic.
- Biết tổ chức dữ liệu IoT theo mô hình thiết bị – topic – payload.
- Vận dụng MQTT để mô phỏng bài toán giám sát và điều khiển thiết bị IoT.

### Thời hạn và hình thức nộp bài

- **Deadline:** 23:59, Thứ Bảy, ngày 10/10/2026.
- **Hình thức nộp:**
  - Đưa mã nguồn lên GitHub.
  - Gửi liên kết GitHub vào nhóm Zalo chung của lớp.
- **Nội dung cần nộp:**
  - Các file mã nguồn Python theo yêu cầu.
  - File `README.md` hướng dẫn chạy chương trình và cấu hình MQTT broker.

## 2. Yêu cầu môi trường

Sinh viên cần chuẩn bị:

- Python 3.x.
- Thư viện `paho-mqtt`.
- Một MQTT broker đã được cấu hình.
- Một IDE hoặc Visual Studio Code.

Cài đặt thư viện bằng lệnh:

```bash
pip install paho-mqtt
```

## 3. Nội dung thực hành

### Bài 1: Ứng dụng gửi và nhận thông điệp MQTT cơ bản

#### Mục tiêu

Làm quen với cơ chế Publisher/Subscriber trong MQTT.

#### Chương trình 1: Publisher

Tạo file `publisher_bai1.py` với các chức năng:

- Kết nối tới MQTT broker.
- Gửi thông điệp lên topic:

```text
iot/lab/message
```

- Nội dung thông điệp phải gồm:
  - Họ tên sinh viên.
  - Mã sinh viên.
  - Nội dung chào mừng, ví dụ: `Xin chao tu client Python MQTT`.

#### Chương trình 2: Subscriber

Tạo file `subscriber_bai1.py` với các chức năng:

- Kết nối tới cùng MQTT broker với Publisher.
- Đăng ký lắng nghe topic:

```text
iot/lab/message
```

- Khi nhận được thông điệp, in ra màn hình:
  - Topic.
  - Nội dung thông điệp.
  - Thời điểm nhận.

#### Đầu ra tham khảo

```text
Nhan duoc message:
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN001 - Nguyen Van A
Time: 10:15:20
```

#### Gợi ý mở rộng

- Cho phép Publisher gửi nhiều thông điệp liên tiếp.
- Cho Subscriber chạy liên tục đến khi người dùng nhấn `Ctrl+C`.

#### Tiêu chí đánh giá

- Kết nối thành công tới broker.
- Publish đúng topic.
- Subscriber nhận đúng dữ liệu.
- Kết quả được hiển thị rõ ràng.

---

### Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm bằng MQTT

#### Mục tiêu

Mô phỏng thiết bị IoT gửi dữ liệu cảm biến định kỳ.

#### Chương trình 1: Sensor Publisher

Tạo file `sensor_publisher_bai2.py` với các chức năng:

- Mô phỏng một cảm biến gửi dữ liệu mỗi 3 giây.
- Publish dữ liệu lên topic:

```text
iot/lab/sensor01/data
```

- Payload phải ở định dạng JSON và gồm các trường:

```json
{
  "device_id": "sensor01",
  "temperature": 28.5,
  "humidity": 65.2
}
```

- Giá trị nhiệt độ và độ ẩm có thể được sinh ngẫu nhiên trong khoảng hợp lý.

#### Chương trình 2: Monitoring Subscriber

Tạo file `monitor_subscriber_bai2.py` với các chức năng:

- Subscribe topic:

```text
iot/lab/sensor01/data
```

- Nhận và phân tích payload JSON.
- In dữ liệu cảm biến ra màn hình.
- Kiểm tra các ngưỡng cảnh báo:
  - Nếu nhiệt độ lớn hơn `35°C`, in `CANH BAO: Nhiet do cao`.
  - Nếu độ ẩm nhỏ hơn `40%`, in `CANH BAO: Do am thap`.

#### Đầu ra tham khảo

```text
Device: sensor01
Temperature: 36.1 C
Humidity: 38.7 %
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
```

#### Gợi ý mở rộng

- Hiển thị dữ liệu rõ ràng theo từng dòng.
- Gửi dữ liệu của nhiều thiết bị khác nhau như `sensor01`, `sensor02`.

#### Tiêu chí đánh giá

- Payload đúng định dạng JSON.
- Dữ liệu được gửi tuần hoàn.
- Subscriber phân tích được dữ liệu.
- Cảnh báo đúng điều kiện.

---

### Bài 3: Mô phỏng hệ thống điều khiển đèn thông minh qua MQTT

#### Mục tiêu

Xây dựng mô hình IoT hai chiều: giám sát và điều khiển.

#### Chương trình 1: Smart Light Device

Tạo file `device_bai3.py` với các chức năng:

- Subscribe topic điều khiển:

```text
iot/lab/light01/cmd
```

- Publish trạng thái hiện tại lên topic:

```text
iot/lab/light01/status
```

- Xử lý các lệnh:
  - `ON`: chuyển trạng thái đèn thành bật.
  - `OFF`: chuyển trạng thái đèn thành tắt.
- Sau mỗi lệnh hợp lệ, thiết bị phải publish trạng thái mới.
- Payload trạng thái phải ở định dạng JSON, ví dụ:

```json
{
  "device_id": "light01",
  "status": "ON"
}
```

#### Chương trình 2: Controller App

Tạo file `controller_bai3.py` với các chức năng:

- Cho phép người dùng nhập lệnh từ bàn phím:
  - `ON`.
  - `OFF`.
- Publish lệnh lên topic:

```text
iot/lab/light01/cmd
```

- Đồng thời subscribe topic trạng thái:

```text
iot/lab/light01/status
```

- Hiển thị trạng thái đèn sau khi nhận phản hồi.

#### Đầu ra tham khảo

```text
Nhap lenh: ON
Da gui lenh ON toi light01

Trang thai nhan duoc:
{"device_id":"light01","status":"ON"}
```

#### Gợi ý mở rộng

- Nếu người dùng nhập lệnh khác `ON` hoặc `OFF`, chương trình phải báo lỗi.
- Thêm lệnh `EXIT` để kết thúc chương trình.
- Mô phỏng nhiều thiết bị như `light01`, `fan01`, `pump01`.

#### Tiêu chí đánh giá

- Điều khiển được thiết bị qua MQTT.
- Thiết bị phản hồi đúng trạng thái.
- Có cơ chế giao tiếp hai chiều.
- Topic được tổ chức hợp lý.

## 4. Yêu cầu nộp bài

Mỗi sinh viên hoặc nhóm cần nộp đầy đủ các file sau:

```text
publisher_bai1.py
subscriber_bai1.py
sensor_publisher_bai2.py
monitor_subscriber_bai2.py
device_bai3.py
controller_bai3.py
README.md
requirements.md
```

File `README.md` cần mô tả ngắn gọn:

- MQTT broker được sử dụng.
- Cách cấu hình MQTT broker.
- Cách cài đặt thư viện cần thiết.
- Cách chạy từng chương trình.
- Kết quả đạt được.

## 5. Bảng tổng hợp topic MQTT

| Bài | Chương trình | Loại | Topic |
|---|---|---|---|
| 1 | Publisher | Publish | `iot/lab/message` |
| 1 | Subscriber | Subscribe | `iot/lab/message` |
| 2 | Sensor Publisher | Publish | `iot/lab/sensor01/data` |
| 2 | Monitoring Subscriber | Subscribe | `iot/lab/sensor01/data` |
| 3 | Smart Light Device | Subscribe | `iot/lab/light01/cmd` |
| 3 | Smart Light Device | Publish | `iot/lab/light01/status` |
| 3 | Controller App | Publish | `iot/lab/light01/cmd` |
| 3 | Controller App | Subscribe | `iot/lab/light01/status` |

## 6. Điều kiện hoàn thành

Bài thực hành được xem là hoàn thành khi:

- Có đủ sáu chương trình Python theo đúng tên file yêu cầu.
- Các chương trình kết nối được tới MQTT broker đã cấu hình.
- Publisher và Subscriber sử dụng đúng topic.
- Payload JSON ở Bài 2 và Bài 3 hợp lệ.
- Chức năng cảnh báo ở Bài 2 hoạt động đúng ngưỡng.
- Chức năng điều khiển và phản hồi trạng thái ở Bài 3 hoạt động hai chiều.
- Repository GitHub có tài liệu hướng dẫn chạy và cấu hình broker.
