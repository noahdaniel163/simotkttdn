from pydantic import BaseModel

class Simo001Payload(BaseModel):
    Cif: str
    TenToChuc: str
    SoGiayPhepThanhLap: str
    LoaiGiayToThanhLapToChuc: int
    NgayThanhLap: str
    DiaChiToChuc: str
    HoTenNguoiDaiDien: str
    SoGiayToTuyThan: str
    LoaiGiayToTuyThan: int
    NgaySinh: str
    GioiTinh: int
    QuocTich: str
    DienThoai: str
    SoTaiKhoanToChuc: str
    NgayMoTaiKhoan: str
    TrangThaiTaiKhoan: int
    DiaChiMAC: str
    SO_IMEI: str

class Simo002Payload(BaseModel):
    Cif: str
    TenToChuc: str
    SoGiayPhepThanhLap: str
    SoTaiKhoanToChuc: str
    TrangThaiTaiKhoan: int
    NghiNgo: int

class Simo003Payload(BaseModel):
    Cif: str
    TenToChuc: str
    SoGiayPhepThanhLap: str
    SoTaiKhoanToChuc: str
    TrangThaiTaiKhoan: int
    NghiNgo: int
    LyDoCapNhat: str

class Simo004Payload(BaseModel):
    Cif: str
    TenToChuc: str
    SoGiayPhepThanhLap: str
    LoaiGiayToThanhLapToChuc: int
    NgayThanhLap: str
    DiaChiToChuc: str
    HoTenNguoiDaiDien: str
    SoGiayToTuyThan: str
    LoaiGiayToTuyThan: int
    NgaySinh: str
    GioiTinh: int
    QuocTich: str
    DienThoai: str
    SoTaiKhoanToChuc: str
    NgayMoTaiKhoan: str
    TrangThaiTaiKhoan: int
    DiaChiMAC: str
    SO_IMEI: str
