# Thực hành Python với giao thức MQTT

Repository này dùng cho buổi thực hành lập trình Python với MQTT, gồm các bài tập publish/subscribe, mô phỏng cảm biến và điều khiển thiết bị IoT.

Nội dung yêu cầu chi tiết được trình bày trong file [`requirements.md`](requirements.md).

## 1. Yêu cầu hệ thống

Trước khi bắt đầu, cần cài đặt:

- Python 3.x.
- `pip` (thường được cài kèm Python).
- Git nếu tải dự án từ GitHub.
- Một MQTT broker, ví dụ Mosquitto, hoặc thông tin của một broker có sẵn.
- Visual Studio Code hoặc IDE Python bất kỳ.

Kiểm tra Python và `pip`:

```bash
python --version
python -m pip --version
```

> Trên một số máy macOS/Linux, lệnh Python có thể là `python3` thay vì `python`.

## 2. Tải mã nguồn

Clone repository từ GitHub:

```bash
git clone <DUONG_DAN_GITHUB_CUA_DU_AN>
cd IOT_ThucHanh_01
```

Nếu không sử dụng Git, có thể tải file ZIP từ GitHub và giải nén vào một thư mục trên máy.

## 3. Tạo môi trường ảo

Môi trường ảo giúp các thư viện của dự án không ảnh hưởng tới những dự án Python khác.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script kích hoạt, chạy lệnh sau trong cửa sổ PowerShell hiện tại rồi kích hoạt lại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sau khi kích hoạt thành công, tên môi trường `(.venv)` thường xuất hiện ở đầu dòng lệnh.

## 4. Cài đặt thư viện

Khi môi trường ảo đã được kích hoạt, cài toàn bộ thư viện từ `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Trên macOS/Linux, nếu không có lệnh `python`, sử dụng:

```bash
python3 -m pip install -r requirements.txt
```

Thư viện chính của dự án:

```text
paho-mqtt==2.1.0
```

Kiểm tra cài đặt:

```bash
python -c "import paho.mqtt; print(paho.mqtt.__version__)"
```

Nếu kết quả hiển thị `2.1.0`, thư viện đã được cài thành công.

## 5. Cấu hình MQTT broker

Các chương trình Publisher và Subscriber phải sử dụng cùng một broker, cổng và cấu hình xác thực.

Các thông số thường dùng:

| Thông số | Ví dụ | Ý nghĩa |
|---|---|---|
| Host | `localhost` | Địa chỉ MQTT broker |
| Port | `1883` | Cổng MQTT không sử dụng TLS |
| Username | Để trống hoặc theo broker | Tên đăng nhập |
| Password | Để trống hoặc theo broker | Mật khẩu |
| Keep Alive | `60` | Thời gian duy trì kết nối, tính bằng giây |

### Lựa chọn A: Mosquitto chạy trên máy cá nhân

1. Cài đặt Eclipse Mosquitto từ trang chính thức hoặc trình quản lý gói của hệ điều hành.
2. Khởi động Mosquitto trên cổng mặc định `1883`.
3. Cấu hình các chương trình Python:

```python
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
```

Để chạy broker ở chế độ hiển thị log:

```bash
mosquitto -v
```

> Cách khởi động dịch vụ Mosquitto có thể khác nhau tùy hệ điều hành và cách cài đặt.

### Lựa chọn B: Broker do giảng viên cung cấp

Cập nhật địa chỉ, cổng, tên đăng nhập và mật khẩu trong các file Python theo thông tin được cung cấp:

```python
MQTT_BROKER = "dia-chi-broker"
MQTT_PORT = 1883
MQTT_USERNAME = "ten-dang-nhap"
MQTT_PASSWORD = "mat-khau"
```

Nếu broker yêu cầu xác thực, cấu hình client trước khi kết nối:

```python
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
```

Không đưa mật khẩu thật lên GitHub. Nên sử dụng biến môi trường hoặc file cấu hình cục bộ đã được thêm vào `.gitignore`.

## 6. Các topic sử dụng

| Bài | Topic | Mục đích |
|---|---|---|
| 1 | `iot/lab/message` | Gửi và nhận thông điệp cơ bản |
| 2 | `iot/lab/sensor01/data` | Gửi dữ liệu nhiệt độ và độ ẩm |
| 3 | `iot/lab/light01/cmd` | Gửi lệnh điều khiển đèn |
| 3 | `iot/lab/light01/status` | Phản hồi trạng thái đèn |

## 7. Cách chạy chương trình

Luôn chạy Subscriber hoặc thiết bị nhận lệnh trước, sau đó mới chạy Publisher hoặc ứng dụng điều khiển.

### Bài 1

Mở terminal thứ nhất:

```bash
python subscriber_bai1.py
```

Mở terminal thứ hai:

```bash
python publisher_bai1.py
```

### Bài 2

Mở terminal thứ nhất:

```bash
python monitor_subscriber_bai2.py
```

Mở terminal thứ hai:

```bash
python sensor_publisher_bai2.py
```

### Bài 3

Mở terminal thứ nhất:

```bash
python device_bai3.py
```

Mở terminal thứ hai:

```bash
python controller_bai3.py
```

> Các file chương trình cần được tạo đầy đủ trước khi thực hiện các lệnh trên.

Nhấn `Ctrl+C` để dừng một chương trình đang chạy liên tục. Với chương trình Controller, có thể nhập `EXIT` nếu chức năng này đã được cài đặt.

## 8. Thoát môi trường ảo

Sau khi hoàn thành, chạy:

```bash
deactivate
```

## 9. Cài đặt dự án trên máy khác

Không sao chép thư mục `.venv` sang máy khác vì môi trường ảo phụ thuộc vào hệ điều hành và đường dẫn cài đặt. Chỉ cần sao chép hoặc clone repository, sau đó chạy lại:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## 10. Xử lý lỗi thường gặp

### Không tìm thấy lệnh `python`

- Cài Python 3 từ nguồn phù hợp với hệ điều hành.
- Trên Windows, chọn tùy chọn **Add Python to PATH** khi cài đặt.
- Trên macOS/Linux, thử sử dụng `python3`.

### Không kích hoạt được môi trường ảo trên PowerShell

Chạy:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Sau đó chạy lại:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Lỗi `ModuleNotFoundError: No module named 'paho'`

Đảm bảo môi trường ảo đã được kích hoạt và chạy:

```bash
python -m pip install -r requirements.txt
```

### Không kết nối được MQTT broker

Kiểm tra:

- Broker đã được khởi động hay chưa.
- Địa chỉ host và cổng có chính xác không.
- Publisher và Subscriber có dùng cùng broker không.
- Firewall có chặn cổng MQTT không.
- Broker có yêu cầu username, password hoặc TLS không.

## 11. Danh sách file cần nộp

```text
publisher_bai1.py
subscriber_bai1.py
sensor_publisher_bai2.py
monitor_subscriber_bai2.py
device_bai3.py
controller_bai3.py
requirements.txt
requirements.md
README.md
```

Không đưa thư mục `.venv` lên GitHub. Thư mục này đã được khai báo trong `.gitignore` và có thể được tạo lại từ `requirements.txt`.
