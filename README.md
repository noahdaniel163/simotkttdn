# SIMO KHDN FastAPI - Hệ thống gửi báo cáo khách hàng tổ chức qua API SBV

## Mục đích
Ứng dụng này giúp gửi dữ liệu báo cáo các mã SIMO (001, 002, 003, 004) lên hệ thống SBV qua API, hỗ trợ nhập liệu, kiểm thử, log kết quả và lỗi, giao diện web thân thiện.

## Tính năng chính
- Giao diện web UI hiện đại, trực quan, hỗ trợ cả tìm kiếm realtime (AJAX) và tìm kiếm server-side render (SSR).
- Tìm kiếm, lọc, chọn nhiều dòng dữ liệu từ database (SQL Server) với bảng TKTT_TOCHUC.
- Chọn mã nghiệp vụ SIMO (001/002/003/004), xuất JSON đúng schema hoặc gửi trực tiếp lên endpoint SBV.
- Hỗ trợ nhập liệu, kiểm thử, log kết quả/lỗi, thao tác qua giao diện web.
- Tạo nhanh dữ liệu mẫu cho từng mã SIMO.
- Gửi dữ liệu lên endpoint SBV qua FastAPI backend.
- Log chi tiết từng lần gửi (payload, response, header, lỗi) vào file riêng cho từng mã.
- Cấu hình endpoint, tài khoản qua biến môi trường.
- Hỗ trợ chuyển đổi Excel sang JSON và tải file mẫu.
- Giao diện đẹp, responsive, có hiệu ứng loading, highlight từ khóa, phân trang.

## Cấu trúc thư mục
- `main.py`         : Khởi tạo FastAPI, route UI, đọc dữ liệu mẫu.
- `routes.py`       : Định nghĩa các endpoint gửi dữ liệu, API tìm kiếm, SSR, AJAX, xuất/gửi dữ liệu, log, health check.
- `models.py`       : Định nghĩa schema dữ liệu cho từng mã SIMO.
- `db_utils.py`     : Kết nối, truy vấn SQL Server, tìm kiếm tương đối, chuẩn hóa dữ liệu.
- `auth.py`         : Hàm lấy token từ SBV.
- `config.py`       : Cấu hình endpoint, tài khoản, lấy từ biến môi trường.
- `templates/`      : Giao diện web (base.html, home.html, data_process.html, data_result_ssr.html, ...), dữ liệu mẫu (sample_data.json).
- `logs/`           : Thư mục chứa log gửi nhận cho từng mã SIMO.

## Hướng dẫn sử dụng
### 1. Cài đặt
- Yêu cầu Python 3.10+ và pip.
- Cài đặt thư viện:
  ```bash
  pip install fastapi uvicorn requests jinja2 pyodbc
  ```

### 2. Thiết lập biến môi trường (tùy chọn)
Bạn có thể cấu hình endpoint, tài khoản qua biến môi trường, ví dụ:
```bash
set SIMO_USERNAME=your_user
set SIMO_PASSWORD=your_pass
set SIMO_CONSUMER_KEY=your_key
set SIMO_CONSUMER_SECRET=your_secret
set SIMO_TOKEN_URL=https://...
set SIMO_ENTRYPOINT_URL_001=https://...
```
Nếu không thiết lập, hệ thống sẽ dùng giá trị mặc định.

### 3. Chạy server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Truy cập giao diện
- Mở trình duyệt, truy cập: http://localhost:8000/
- Chọn mã SIMO, nhập hoặc upload file JSON, nhấn "Gửi dữ liệu" (giao diện home).
- Truy cập http://localhost:8000/data-process để sử dụng giao diện tìm kiếm dữ liệu database:
  - Có 2 phương thức tìm kiếm:
    - **Tìm kiếm SSR:** Form đầu trang, submit sẽ chuyển sang trang kết quả đẹp (`/data-result-ssr`) với bảng dữ liệu, chọn dòng, xuất JSON/gửi SBV.
    - **Tìm kiếm AJAX:** Form bên dưới, kết quả hiển thị realtime ngay trên trang, có phân trang, highlight, loading.
- Có thể chọn nhiều dòng, chọn mã SIMO, xuất JSON đúng schema hoặc gửi trực tiếp lên endpoint SBV.

### 5. Kiểm tra log
- Mỗi lần gửi, log ghi vào `logs/simo_00x.log.txt` (x là mã SIMO).
- Log gồm: thời gian, payload, response, header, lỗi (nếu có).
- Log token lưu tại `logs/token.log.txt`.

### 6. Chuyển đổi Excel/JSON
- Tải file Excel mẫu hoặc chuyển đổi Excel sang JSON tại menu "Xử lý Excel".

## Hướng dẫn tạo file kết nối Database và Endpoint

### 1. Kết nối Database SQL Server
- Tạo file `db_config.py` (đã có sẵn mẫu, không commit lên git):
```python
import os
DB_SERVER = os.getenv("SIMO_DB_SERVER", "<Your IP Database Server>")
DB_NAME = os.getenv("SIMO_DB_NAME", "simo")
DB_USER = os.getenv("SIMO_DB_USER", "sa")
DB_PASSWORD = os.getenv("SIMO_DB_PASSWORD", "<Your Database connect passwd sa>")
```
- Tạo file `db_utils.py` để truy vấn:
```python
import pyodbc
from db_config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD

def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"
    )
    return pyodbc.connect(conn_str)

def search_tktt_tochuc(**kwargs):
    query = "SELECT * FROM TKTT_TOCHUC WHERE 1=1"
    params = []
    for field, value in kwargs.items():
        if value is not None and value != "":
            query += f" AND LOWER(REPLACE({field}, ' ', '')) LIKE ?"
            params.append(f"%{''.join(value.lower().split())}%")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results
```
- Đảm bảo file `db_config.py` nằm trong `.gitignore` để bảo mật thông tin.

### 2. Kết nối Endpoint SBV
- Tạo file `config.py` (hoặc chỉnh sửa):
```python
import os
USERNAME = os.getenv("SIMO_USERNAME", "<YOUR_USERNAME>")
PASSWORD = os.getenv("SIMO_PASSWORD", "<YOUR_PASSWORD>")
CONSUMER_KEY = os.getenv("SIMO_CONSUMER_KEY", "<YOUR_CONSUMER_KEY>")
CONSUMER_SECRET = os.getenv("SIMO_CONSUMER_SECRET", "<YOUR_CONSUMER_SECRET>")
TOKEN_URL = os.getenv("SIMO_TOKEN_URL", "https://...")
ENTRYPOINT_URL_001 = os.getenv("SIMO_ENTRYPOINT_URL_001", "https://...")
ENTRYPOINT_URL_002 = os.getenv("SIMO_ENTRYPOINT_URL_002", "https://...")
ENTRYPOINT_URL_003 = os.getenv("SIMO_ENTRYPOINT_URL_003", "https://...")
ENTRYPOINT_URL_004 = os.getenv("SIMO_ENTRYPOINT_URL_004", "https://...")
```
- Thông tin endpoint, tài khoản có thể cấu hình qua biến môi trường hoặc sửa trực tiếp file này.

- Đảm bảo file `config.py` nằm trong `.gitignore` để bảo mật thông tin.

## Hướng dẫn tạo cấu trúc bảng TKTT_TOCHUC trong Database SQL Server

### 1. Tạo bảng TKTT_TOCHUC
Sử dụng lệnh SQL sau để tạo bảng và các trường đúng định dạng:

```sql
CREATE TABLE TKTT_TOCHUC (
    Cif NVARCHAR(50),
    TenToChuc NVARCHAR(255),
    SoGiayPhepThanhLap NVARCHAR(50),
    LoaiGiayToThanhLapToChuc INT,
    NgayThanhLap NVARCHAR(20),
    DiaChiToChuc NVARCHAR(255),
    HoTenNguoiDaiDien NVARCHAR(100),
    SoGiayToTuyThan NVARCHAR(50),
    LoaiGiayToTuyThan INT,
    NgaySinh NVARCHAR(20),
    GioiTinh INT,
    QuocTich NVARCHAR(50),
    DienThoai NVARCHAR(30),
    SoTaiKhoanToChuc NVARCHAR(50),
    NgayMoTaiKhoan NVARCHAR(20),
    TrangThaiTaiKhoan INT,
    DiaChiMAC NVARCHAR(50),
    SO_IMEI NVARCHAR(50),
    NghiNgo INT,
    LyDoCapNhat NVARCHAR(255),
    UpdateDate DATETIME
);
```

### 2. Định nghĩa các trường
- **Cif**: Mã định danh tổ chức, kiểu NVARCHAR(50)
- **TenToChuc**: Tên tổ chức, kiểu NVARCHAR(255)
- **SoGiayPhepThanhLap**: Số giấy phép thành lập, kiểu NVARCHAR(50)
- **LoaiGiayToThanhLapToChuc**: Loại giấy tờ thành lập, kiểu INT
- **NgayThanhLap**: Ngày thành lập, kiểu NVARCHAR(20)
- **DiaChiToChuc**: Địa chỉ tổ chức, kiểu NVARCHAR(255)
- **HoTenNguoiDaiDien**: Họ tên người đại diện, kiểu NVARCHAR(100)
- **SoGiayToTuyThan**: Số giấy tờ tùy thân, kiểu NVARCHAR(50)
- **LoaiGiayToTuyThan**: Loại giấy tờ tùy thân, kiểu INT
- **NgaySinh**: Ngày sinh người đại diện, kiểu NVARCHAR(20)
- **GioiTinh**: Giới tính, kiểu INT (1: Nam, 2: Nữ)
- **QuocTich**: Quốc tịch, kiểu NVARCHAR(50)
- **DienThoai**: Số điện thoại, kiểu NVARCHAR(30)
- **SoTaiKhoanToChuc**: Số tài khoản tổ chức, kiểu NVARCHAR(50)
- **NgayMoTaiKhoan**: Ngày mở tài khoản, kiểu NVARCHAR(20)
- **TrangThaiTaiKhoan**: Trạng thái tài khoản, kiểu INT
- **DiaChiMAC**: Địa chỉ MAC, kiểu NVARCHAR(50)
- **SO_IMEI**: Số IMEI, kiểu NVARCHAR(50)
- **NghiNgo**: Cờ nghi ngờ, kiểu INT
- **LyDoCapNhat**: Lý do cập nhật, kiểu NVARCHAR(255)
- **UpdateDate**: Ngày cập nhật, kiểu DATETIME

### 3. Lưu ý bảo mật
- **Không lưu thông tin tài khoản, mật khẩu, endpoint thật trong file README hoặc source code.**
- Thông tin kết nối database và endpoint chỉ nên cấu hình qua biến môi trường hoặc file cấu hình riêng, đã được hướng dẫn ở trên.

## API Reference
- Các endpoint `/simo_001/`, `/simo_002/`, `/simo_003/`, `/simo_004/` nhận payload đúng schema, gửi dữ liệu lên SBV.
- API `/data/tktt_tochuc` hỗ trợ tìm kiếm tương đối, không phân biệt hoa thường, bỏ khoảng trắng, trả về JSON.
- API `/data/export-json` và `/data/send-sbv` nhận danh sách dòng và mã simo, xuất JSON đúng schema hoặc gửi lên endpoint tương ứng.

## Lưu ý
- Ứng dụng chỉ phục vụ kiểm thử, nhập liệu, không thay thế hệ thống chính thức.
- Đảm bảo bảo mật thông tin tài khoản, endpoint khi triển khai thực tế.
- Nếu trường dữ liệu int bị None sẽ được tự động chuyển thành 0 khi xuất/gửi dữ liệu.
- Nếu truy vấn trả về datetime sẽ tự động chuyển thành chuỗi ISO để tránh lỗi khi render.

---
Mọi thắc mắc hoặc góp ý, vui lòng liên hệ đội phát triển.