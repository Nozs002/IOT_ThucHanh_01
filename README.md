# Thực hành Python với giao thức MQTT trên Windows

Repository này dùng cho buổi thực hành lập trình Python với MQTT trên Windows, gồm các nội dung publish/subscribe, mô phỏng cảm biến và điều khiển thiết bị IoT.

Xem yêu cầu chi tiết của bài thực hành tại [`requirements.md`](requirements.md).

## 1. Phần mềm cần cài đặt

Máy tính cần có:

- Windows 10 hoặc Windows 11.
- Python 3.x.
- `pip` và `venv` (được cài kèm Python).
- Git for Windows nếu tải và quản lý dự án bằng Git.
- Visual Studio Code hoặc một IDE Python bất kỳ.
- MQTT broker Mosquitto hoặc thông tin broker do giảng viên cung cấp.

### Kiểm tra Python

Mở PowerShell trong Windows Terminal hoặc Visual Studio Code và chạy:

```powershell
python --version
python -m pip --version
```

Nếu Windows không nhận lệnh `python`, hãy cài Python và chọn tùy chọn **Add Python to PATH** trong quá trình cài đặt.

## 2. Tải mã nguồn

Clone repository bằng PowerShell:

```powershell
git clone https://github.com/Nozs002/IOT_ThucHanh_01.git
cd IOT_ThucHanh_01
```

## 3. Tạo môi trường ảo

Tại thư mục gốc của dự án, chạy:

```powershell
python -m venv .venv
```

Kích hoạt môi trường ảo trong PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Nếu PowerShell chặn script kích hoạt

Chỉ cho phép chạy script trong cửa sổ PowerShell hiện tại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Thiết lập này hết hiệu lực khi đóng cửa sổ PowerShell.

### Kích hoạt bằng Command Prompt

Nếu sử dụng Command Prompt thay cho PowerShell:

```bat
.venv\Scripts\activate.bat
```

## 4. Cài đặt thư viện Python

Sau khi kích hoạt môi trường ảo, chạy:

```powershell
python -m pip install -r requirements.txt
```

Dự án hiện sử dụng:

```text
paho-mqtt==2.1.0
```

Kiểm tra thư viện đã được cài đặt:

```powershell
python -c "import paho.mqtt; print(paho.mqtt.__version__)"
```

Nếu kết quả hiển thị `2.1.0`, môi trường đã sẵn sàng.

## 5. Cấu hình MQTT broker trên Windows

Publisher và Subscriber phải sử dụng cùng địa chỉ broker, cổng và thông tin xác thực.

Thông số phổ biến khi Mosquitto chạy trên cùng máy:

| Thông số | Giá trị |
|---|---|
| Broker host | `localhost` |
| Broker port | `1883` |
| Keep alive | `60` giây |

### Cách 1: Cài Mosquitto trên máy

1. Tải bộ cài Eclipse Mosquitto dành cho Windows.
2. Chạy bộ cài và hoàn tất quá trình cài đặt.
3. Mở PowerShell tại thư mục cài Mosquitto, thường là:

```powershell
cd "C:\Program Files\mosquitto"
```

4. Khởi động broker ở chế độ hiển thị log:

```powershell
.\mosquitto.exe -v
```

5. Giữ cửa sổ này chạy trong khi thử nghiệm các chương trình Python.

Cấu hình tương ứng trong mã Python:

```python
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
```

### Cách 2: Sử dụng broker do giảng viên cung cấp

Cập nhật các thông số trong chương trình theo thông tin được cung cấp:

```python
MQTT_BROKER = "dia-chi-broker"
MQTT_PORT = 1883
MQTT_USERNAME = "ten-dang-nhap"
MQTT_PASSWORD = "mat-khau"
```

Nếu broker yêu cầu xác thực, thiết lập tài khoản trước khi kết nối:

```python
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
```

Không đưa mật khẩu thật lên GitHub. Nên sử dụng biến môi trường hoặc file cấu hình cục bộ đã được thêm vào `.gitignore`.

## 6. Các topic MQTT của bài thực hành

| Bài | Topic | Mục đích |
|---|---|---|
| 1 | `iot/lab/message` | Gửi và nhận thông điệp cơ bản |
| 2 | `iot/lab/sensor01/data` | Gửi dữ liệu nhiệt độ và độ ẩm |
| 3 | `iot/lab/light01/cmd` | Gửi lệnh điều khiển đèn |
| 3 | `iot/lab/light01/status` | Phản hồi trạng thái đèn |

## 7. Chạy các chương trình

Mỗi chương trình cần chạy trong một cửa sổ PowerShell riêng. Hãy kích hoạt `.venv` trong từng cửa sổ trước khi chạy chương trình:

```powershell
.\.venv\Scripts\Activate.ps1
```

Luôn chạy Subscriber hoặc thiết bị nhận lệnh trước, sau đó chạy Publisher hoặc Controller.

### Bài 1: Publisher và Subscriber cơ bản

Terminal thứ nhất:

```powershell
python subscriber_bai1.py
```

Terminal thứ hai:

```powershell
python publisher_bai1.py
```

### Bài 2: Cảm biến nhiệt độ và độ ẩm

Terminal thứ nhất:

```powershell
python monitor_subscriber_bai2.py
```

Terminal thứ hai:

```powershell
python sensor_publisher_bai2.py
```

### Bài 3: Điều khiển đèn thông minh

Terminal thứ nhất:

```powershell
python device_bai3.py
```

Terminal thứ hai:

```powershell
python controller_bai3.py
```

Nhấn `Ctrl+C` để dừng chương trình đang chạy liên tục. Với Controller, có thể nhập `EXIT` nếu chức năng này đã được cài đặt.

> Các file Python cần được tạo đầy đủ trước khi thực hiện các lệnh trên.

## 8. Thoát môi trường ảo

Chạy lệnh sau khi hoàn thành:

```powershell
deactivate
```

## 9. Cài đặt dự án trên một máy Windows khác

Không sao chép thư mục `.venv` sang máy khác. Môi trường ảo cần được tạo lại trên từng máy từ file `requirements.txt`.

Sau khi clone hoặc sao chép repository, mở PowerShell trong thư mục dự án và chạy:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Sau đó cấu hình địa chỉ MQTT broker trong các chương trình Python và chạy theo hướng dẫn ở phần trên.

## 10. Xử lý lỗi thường gặp

### Lỗi `python is not recognized`

- Cài Python 3.
- Chọn **Add Python to PATH** khi cài đặt.
- Đóng và mở lại PowerShell sau khi cài.

### Không kích hoạt được `.venv`

Chạy:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Lỗi `No module named 'paho'`

Đảm bảo `.venv` đã được kích hoạt, sau đó chạy:

```powershell
python -m pip install -r requirements.txt
```

### Không kết nối được MQTT broker

Kiểm tra:

- Mosquitto đã được khởi động chưa.
- Địa chỉ host và cổng có chính xác không.
- Publisher và Subscriber có sử dụng cùng broker không.
- Windows Defender Firewall có chặn cổng `1883` không.
- Broker có yêu cầu username, password hoặc TLS không.

### Cổng `1883` đang được sử dụng

Kiểm tra tiến trình đang sử dụng cổng:

```powershell
netstat -ano | findstr :1883
```

Nếu Mosquitto đã chạy dưới dạng Windows Service thì không cần mở thêm một tiến trình `mosquitto.exe` khác.

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

Không đưa thư mục `.venv` lên GitHub. Thư mục này đã được khai báo trong `.gitignore` và có thể tạo lại từ `requirements.txt`.
