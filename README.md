# SIMO KHDN FastAPI - Hệ thống gửi báo cáo khách hàng tổ chức qua API SBV

## Mục đích
Ứng dụng này giúp gửi dữ liệu báo cáo các mã SIMO (001, 002, 003, 004) lên hệ thống SBV qua API, hỗ trợ nhập liệu, kiểm thử, log kết quả và lỗi, giao diện web thân thiện.

## Tính năng chính
- Giao diện web UI (HTML5, CSS, JS) cho phép chọn mã SIMO, dán hoặc upload file JSON payload.
- Tạo nhanh dữ liệu mẫu cho từng mã SIMO.
- Gửi dữ liệu lên endpoint SBV qua backend FastAPI.
- Log đầy đủ request, response, header, lỗi vào file txt riêng cho từng mã.
- Dễ dàng cấu hình endpoint và tài khoản qua biến môi trường.

## Cấu trúc thư mục
- `main.py`         : Khởi tạo FastAPI, route UI, đọc dữ liệu mẫu.
- `routes.py`       : Định nghĩa các endpoint /simo_001/, /simo_002/, ... gửi dữ liệu lên SBV.
- `models.py`       : Định nghĩa schema dữ liệu cho từng mã SIMO.
- `auth.py`         : Hàm lấy token từ SBV.
- `config.py`       : Cấu hình endpoint, tài khoản, lấy từ biến môi trường.
- `templates/`      : Giao diện web (base.html, home.html), dữ liệu mẫu (sample_data.json).
- `logs/`           : Thư mục chứa log gửi nhận cho từng mã SIMO.

## Hướng dẫn sử dụng
### 1. Cài đặt
- Yêu cầu Python 3.10+ và pip.
- Cài đặt thư viện:
  ```bash
  pip install fastapi uvicorn requests jinja2
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
- Mở trình duyệt, truy cập: http://localhost:8000/ (hoặc http://<ip_máy_chủ>:8000/ trong LAN)
- Chọn mã SIMO, dán payload hoặc upload file JSON, nhấn "Gửi dữ liệu".
- Xem kết quả trả về từ endpoint ngay trên giao diện.
- Có thể bấm "Tạo data mẫu" để lấy nhanh dữ liệu mẫu.

### 5. Kiểm tra log
- Mỗi lần gửi dữ liệu, log sẽ được ghi vào file `logs/simo_00x.log.txt`.
- Log gồm: thời gian, payload gửi đi, response, header nhận được, lỗi (nếu có).

## Mở rộng
- Có thể chỉnh sửa file `templates/sample_data.json` để thay đổi dữ liệu mẫu.
- Có thể chỉnh sửa giao diện trong `templates/base.html`, `templates/home.html`.
- Có thể thêm các mã SIMO mới bằng cách bổ sung model, route tương ứng.

## Lưu ý
- Ứng dụng chỉ là công cụ hỗ trợ nhập liệu, kiểm thử, không thay thế hệ thống vận hành chính thức.
- Đảm bảo bảo mật thông tin tài khoản, endpoint khi triển khai thực tế.

## API Reference

### 1. Endpoint: `/simo_001/` (POST)
- **Mục đích:** Gửi báo cáo danh sách tài khoản thanh toán KHDN (SIMO 001)
- **Payload Schema:**
  ```json
  [
    {
      "Cif": "string",
      "TenToChuc": "string",
      "SoGiayPhepThanhLap": "string",
      "LoaiGiayToThanhLapToChuc": 1,
      "NgayThanhLap": "dd/MM/yyyy",
      "DiaChiToChuc": "string",
      "HoTenNguoiDaiDien": "string",
      "SoGiayToTuyThan": "string",
      "LoaiGiayToTuyThan": 1,
      "NgaySinh": "dd/MM/yyyy",
      "GioiTinh": 1,
      "QuocTich": "string",
      "DienThoai": "string",
      "SoTaiKhoanToChuc": "string",
      "NgayMoTaiKhoan": "dd/MM/yyyy",
      "TrangThaiTaiKhoan": 1,
      "DiaChiMAC": "string",
      "SO_IMEI": "string"
    }
  ]
  ```
- **Ví dụ:**
  ```json
  [
    {
      "Cif": "123456789012345678901234567890123456",
      "TenToChuc": "Công ty TNHH ABC",
      "SoGiayPhepThanhLap": "123456789012345",
      "LoaiGiayToThanhLapToChuc": 1,
      "NgayThanhLap": "01/01/2020",
      "DiaChiToChuc": "123 Đường Láng, Đống Đa, Hà Nội",
      "HoTenNguoiDaiDien": "Nguyễn Văn A",
      "SoGiayToTuyThan": "123456789012",
      "LoaiGiayToTuyThan": 1,
      "NgaySinh": "15/05/1980",
      "GioiTinh": 1,
      "QuocTich": "Việt Nam",
      "DienThoai": "0987654321",
      "SoTaiKhoanToChuc": "12345678901234567890",
      "NgayMoTaiKhoan": "01/02/2021",
      "TrangThaiTaiKhoan": 1,
      "DiaChiMAC": "001A2B3C4D5E",
      "SO_IMEI": "123456789012345"
    }
  ]
  ```

### 2. Endpoint: `/simo_002/` (POST)
- **Mục đích:** Gửi báo cáo danh sách tài khoản nghi ngờ KHDN (SIMO 002)
- **Payload Schema:**
  ```json
  [
    {
      "Cif": "string",
      "TenToChuc": "string",
      "SoGiayPhepThanhLap": "string",
      "SoTaiKhoanToChuc": "string",
      "TrangThaiTaiKhoan": 1,
      "NghiNgo": 1,
      "GhiChu": "string"
    }
  ]
  ```
- **Ví dụ:**
  ```json
  [
    {
      "Cif": "123456789012345678901234567890123456",
      "TenToChuc": "Công ty TNHH XYZ",
      "SoGiayPhepThanhLap": "987654321012345",
      "SoTaiKhoanToChuc": "09876543210987654321",
      "TrangThaiTaiKhoan": 3,
      "NghiNgo": 1,
      "GhiChu": "Thông tin hồ sơ không khớp với Cơ sở dữ liệu quốc gia về đăng ký doanh nghiệp."
    }
  ]
  ```

### 3. Endpoint: `/simo_003/` (POST)
- **Mục đích:** Gửi báo cáo cập nhật trạng thái tài khoản nghi ngờ KHDN (SIMO 003)
- **Payload Schema:**
  ```json
  [
    {
      "Cif": "string",
      "TenToChuc": "string",
      "SoGiayPhepThanhLap": "string",
      "SoTaiKhoanToChuc": "string",
      "TrangThaiTaiKhoan": 1,
      "NghiNgo": 1,
      "LyDoCapNhat": "string"
    }
  ]
  ```
- **Ví dụ:**
  ```json
  [
    {
      "Cif": "123456789012345678901234567890123456",
      "TenToChuc": "Công ty TNHH XYZ",
      "SoGiayPhepThanhLap": "987654321012345",
      "SoTaiKhoanToChuc": "09876543210987654321",
      "TrangThaiTaiKhoan": 4,
      "NghiNgo": 2,
      "LyDoCapNhat": "Cập nhật trạng thái tài khoản do phát hiện hoạt động giao dịch bất thường."
    }
  ]
  ```

### 4. Endpoint: `/simo_004/` (POST)
- **Mục đích:** Gửi báo cáo cập nhật danh sách tài khoản KHDN (SIMO 004)
- **Payload Schema:**
  ```json
  [
    {
      "Cif": "string",
      "TenToChuc": "string",
      "SoGiayPhepThanhLap": "string",
      "LoaiGiayToThanhLapToChuc": 1,
      "NgayThanhLap": "dd/MM/yyyy",
      "DiaChiToChuc": "string",
      "HoTenNguoiDaiDien": "string",
      "SoGiayToTuyThan": "string",
      "LoaiGiayToTuyThan": 1,
      "NgaySinh": "dd/MM/yyyy",
      "GioiTinh": 1,
      "QuocTich": "string",
      "DienThoai": "string",
      "SoTaiKhoanToChuc": "string",
      "NgayMoTaiKhoan": "dd/MM/yyyy",
      "TrangThaiTaiKhoan": 1,
      "DiaChiMAC": "string",
      "SO_IMEI": "string"
    }
  ]
  ```
- **Ví dụ:**
  ```json
  [
    {
      "Cif": "123456789012345678901234567890123456",
      "TenToChuc": "Công ty TNHH ABC",
      "SoGiayPhepThanhLap": "123456789012345",
      "LoaiGiayToThanhLapToChuc": 1,
      "NgayThanhLap": "01/01/2020",
      "DiaChiToChuc": "123 Đường Láng, Đống Đa, Hà Nội",
      "HoTenNguoiDaiDien": "Nguyễn Văn A",
      "SoGiayToTuyThan": "123456789012",
      "LoaiGiayToTuyThan": 1,
      "NgaySinh": "15/05/1980",
      "GioiTinh": 1,
      "QuocTich": "Việt Nam",
      "DienThoai": "0987654321",
      "SoTaiKhoanToChuc": "12345678901234567890",
      "NgayMoTaiKhoan": "01/02/2021",
      "TrangThaiTaiKhoan": 1,
      "DiaChiMAC": "001A2B3C4D5E",
      "SO_IMEI": "123456789012345"
    }
  ]
  ```

### 5. Response mẫu
- Thành công:
  ```json
  {
    "result": {
      "code": "00",
      "message": "",
      "success": true,
      "result": "done"
    }
  }
  ```
- Lỗi:
  ```json
  {
    "detail": "<thông báo lỗi từ SBV hoặc hệ thống>"
  }
  ```

### 6. Lưu ý khi gửi dữ liệu
- Payload phải là một mảng (list) các object đúng schema từng mã.
- Trường ngày tháng định dạng dd/MM/yyyy.
- Nếu gửi sai schema hoặc thiếu trường bắt buộc, API sẽ trả về lỗi.
- Token được lấy tự động, không cần truyền thủ công.

---
Mọi thắc mắc hoặc góp ý, vui lòng liên hệ đội phát triển.
