from fastapi import APIRouter, HTTPException, Response, Query, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import datetime
import requests
from auth import get_sbv_token
from config import ENTRYPOINT_URL_001, ENTRYPOINT_URL_002, ENTRYPOINT_URL_003, ENTRYPOINT_URL_004
from models import Simo001Payload, Simo002Payload, Simo003Payload, Simo004Payload
import os
from datetime import datetime as dt
import subprocess
from db_utils import search_tktt_tochuc

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def log_to_file(simo_code: str, action: str, data: dict, response: object = None, error: str = None, response_headers: dict = None):
    import json
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"simo_{simo_code}.log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S')}] ACTION: {action}\n")
        f.write(f"Payload: {json.dumps(data, ensure_ascii=False, indent=2)}\n")
        if response_headers is not None:
            f.write(f"Response Headers: {json.dumps(dict(response_headers), ensure_ascii=False, indent=2)}\n")
        if response is not None:
            if isinstance(response, (dict, list)):
                f.write(f"Response: {json.dumps(response, ensure_ascii=False, indent=2)}\n")
            else:
                f.write(f"Response: {str(response)}\n")
        if error is not None:
            f.write(f"Error: {error}\n")
        f.write("-"*60 + "\n")

@router.post("/simo_001/")
def simo_001(payload: list[Simo001Payload]):
    token = get_sbv_token()
    if not token:
        log_to_file('001', 'get_token', {}, error='Không thể lấy token từ SBV')
        raise HTTPException(status_code=500, detail="Không thể lấy token từ SBV")
    now = datetime.datetime.now()
    last_month = now.replace(day=1) - datetime.timedelta(days=1)
    ma_yeu_cau = f"simo001_TKTTDN_{now.strftime('%d%m%H%M%S')}"
    ky_bao_cao = last_month.strftime("%m/%Y")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "maYeuCau": ma_yeu_cau,
        "kyBaoCao": ky_bao_cao
    }
    try:
        resp = requests.post(ENTRYPOINT_URL_001, headers=headers, json=[item.dict() for item in payload], timeout=10)
        resp.raise_for_status()
        log_to_file('001', 'send', [item.dict() for item in payload], response=resp.json(), response_headers=resp.headers)
        return {"result": resp.json()}
    except requests.RequestException as e:
        detail = e.response.text if e.response is not None else str(e)
        headers = e.response.headers if hasattr(e, 'response') and e.response is not None else None
        log_to_file('001', 'send', [item.dict() for item in payload], error=detail, response_headers=headers)
        raise HTTPException(status_code=resp.status_code if 'resp' in locals() else 500, detail=detail)

@router.post("/simo_002/")
def simo_002(payload: list[Simo002Payload]):
    token = get_sbv_token()
    if not token:
        log_to_file('002', 'get_token', {}, error='Không thể lấy token từ SBV')
        raise HTTPException(status_code=500, detail="Không thể lấy token từ SBV")
    now = datetime.datetime.now()
    ma_yeu_cau = f"simo002_TKTTDN_{now.strftime('%d%m%H%M%S')}"
    ky_bao_cao = now.strftime("%m/%Y")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "maYeuCau": ma_yeu_cau,
        "kyBaoCao": ky_bao_cao
    }
    try:
        resp = requests.post(ENTRYPOINT_URL_002, headers=headers, json=[item.dict() for item in payload], timeout=10)
        resp.raise_for_status()
        log_to_file('002', 'send', [item.dict() for item in payload], response=resp.json(), response_headers=resp.headers)
        return {"result": resp.json()}
    except requests.RequestException as e:
        detail = e.response.text if e.response is not None else str(e)
        headers = e.response.headers if hasattr(e, 'response') and e.response is not None else None
        log_to_file('002', 'send', [item.dict() for item in payload], error=detail, response_headers=headers)
        raise HTTPException(status_code=resp.status_code if 'resp' in locals() else 500, detail=detail)

@router.post("/simo_003/")
def simo_003(payload: list[Simo003Payload]):
    token = get_sbv_token()
    if not token:
        log_to_file('003', 'get_token', {}, error='Không thể lấy token từ SBV')
        raise HTTPException(status_code=500, detail="Không thể lấy token từ SBV")
    now = datetime.datetime.now()
    ma_yeu_cau = f"simo003_TKTTDN_{now.strftime('%d%m%H%M%S')}"
    ky_bao_cao = now.strftime("%m/%Y")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "maYeuCau": ma_yeu_cau,
        "kyBaoCao": ky_bao_cao
    }
    try:
        resp = requests.post(ENTRYPOINT_URL_003, headers=headers, json=[item.dict() for item in payload], timeout=10)
        resp.raise_for_status()
        log_to_file('003', 'send', [item.dict() for item in payload], response=resp.json(), response_headers=resp.headers)
        return {"result": resp.json()}
    except requests.RequestException as e:
        detail = e.response.text if e.response is not None else str(e)
        headers = e.response.headers if hasattr(e, 'response') and e.response is not None else None
        log_to_file('003', 'send', [item.dict() for item in payload], error=detail, response_headers=headers)
        raise HTTPException(status_code=resp.status_code if 'resp' in locals() else 500, detail=detail)

@router.post("/simo_004/")
def simo_004(payload: list[Simo004Payload]):
    token = get_sbv_token()
    if not token:
        log_to_file('004', 'get_token', {}, error='Không thể lấy token từ SBV')
        raise HTTPException(status_code=500, detail="Không thể lấy token từ SBV")
    now = datetime.datetime.now()
    ma_yeu_cau = f"simo004_TKTTDN_{now.strftime('%d%m%H%M%S')}"
    ky_bao_cao = now.strftime("%m/%Y")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "maYeuCau": ma_yeu_cau,
        "kyBaoCao": ky_bao_cao
    }
    try:
        resp = requests.post(ENTRYPOINT_URL_004, headers=headers, json=[item.dict() for item in payload], timeout=10)
        resp.raise_for_status()
        log_to_file('004', 'send', [item.dict() for item in payload], response=resp.json(), response_headers=resp.headers)
        return {"result": resp.json()}
    except requests.RequestException as e:
        detail = e.response.text if e.response is not None else str(e)
        headers = e.response.headers if hasattr(e, 'response') and e.response is not None else None
        log_to_file('004', 'send', [item.dict() for item in payload], error=detail, response_headers=headers)
        raise HTTPException(status_code=resp.status_code if 'resp' in locals() else 500, detail=detail)

@router.get("/health/icmp/{host}")
def health_icmp(host: str):
    try:
        # Windows: -n 1, Linux/Mac: -c 1
        param = '-n' if os.name == 'nt' else '-c'
        result = subprocess.run(["ping", param, "1", host], capture_output=True, text=True)
        if result.returncode == 0:
            return {"host": host, "status": "reachable", "output": result.stdout}
        else:
            return Response(content=result.stdout + result.stderr, status_code=503, media_type="text/plain")
    except Exception as e:
        return Response(content=str(e), status_code=500, media_type="text/plain")

@router.get("/health/http/{endpoint}")
def health_http(endpoint: str):
    import requests
    try:
        if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
            endpoint = "http://" + endpoint
        resp = requests.get(endpoint, timeout=5)
        return {"endpoint": endpoint, "status_code": resp.status_code, "reason": resp.reason}
    except Exception as e:
        return Response(content=f"Lỗi: {str(e)}", status_code=503, media_type="text/plain")

@router.get("/data-process")
def data_process_page(request: Request):
    return templates.TemplateResponse("data_process.html", {"request": request})

@router.get("/data-result")
def data_result_page(request: Request):
    return templates.TemplateResponse("data_result.html", {"request": request})

import datetime
import json

def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@router.post("/data-result-ssr")
def data_result_ssr(request: Request,
    Cif: str = Form(None),
    TenToChuc: str = Form(None),
    SoTaiKhoanToChuc: str = Form(None),
    SoGiayPhepThanhLap: str = Form(None)
):
    results = search_tktt_tochuc(
        Cif=Cif,
        TenToChuc=TenToChuc,
        SoTaiKhoanToChuc=SoTaiKhoanToChuc,
        SoGiayPhepThanhLap=SoGiayPhepThanhLap
    )
    # Chuyển đổi datetime về string để tránh lỗi tojson
    for row in results:
        for k, v in row.items():
            if isinstance(v, (datetime.datetime, datetime.date)):
                row[k] = v.isoformat()
    return templates.TemplateResponse("data_result_ssr.html", {"request": request, "results": results})

@router.get("/data/tktt_tochuc")
def data_tktt_tochuc(q: str = Query(None)):
    # Tìm kiếm tương đối theo nhiều trường nếu có từ khóa q
    if q:
        results = search_tktt_tochuc(Cif=q, TenToChuc=q, SoGiayPhepThanhLap=q, HoTenNguoiDaiDien=q, SoTaiKhoanToChuc=q)
    else:
        results = search_tktt_tochuc()
    return {"results": results}

# Helper: mapping row dict sang schema đúng mã simo
SIMO_FIELDS = {
    "001": [f for f in Simo001Payload.schema()['properties'].keys()],
    "002": [f for f in Simo002Payload.schema()['properties'].keys()],
    "003": [f for f in Simo003Payload.schema()['properties'].keys()],
    "004": [f for f in Simo004Payload.schema()['properties'].keys()],
}
def map_row_schema(row, simo_code):
    fields = SIMO_FIELDS.get(simo_code, [])
    return {k: row.get(k, None) for k in fields}

@router.post("/data/export-json")
def export_json_api(data: dict):
    simo_code = data.get("simo_code")
    rows = data.get("rows", [])
    json_data = [map_row_schema(row, simo_code) for row in rows]
    return {"json": json_data}

@router.post("/data/send-sbv")
def send_sbv_api(data: dict):
    simo_code = data.get("simo_code")
    rows = data.get("rows", [])
    json_data = [map_row_schema(row, simo_code) for row in rows]
    # Gọi endpoint tương ứng
    if simo_code == "001":
        return simo_001([Simo001Payload(**item) for item in json_data])
    if simo_code == "002":
        return simo_002([Simo002Payload(**item) for item in json_data])
    if simo_code == "003":
        return simo_003([Simo003Payload(**item) for item in json_data])
    if simo_code == "004":
        return simo_004([Simo004Payload(**item) for item in json_data])
    return JSONResponse({"error": "Mã simo không hợp lệ"}, status_code=400)

@router.get("/data/tktt_tochuc", tags=["Xử lý dữ liệu"])
def search_tktt_tochuc_api(
    Cif: str = Query(None),
    TenToChuc: str = Query(None),
    SoGiayPhepThanhLap: str = Query(None),
    LoaiGiayToThanhLapToChuc: int = Query(None),
    NgayThanhLap: str = Query(None),
    DiaChiToChuc: str = Query(None),
    HoTenNguoiDaiDien: str = Query(None),
    SoGiayToTuyThan: str = Query(None),
    LoaiGiayToTuyThan: int = Query(None),
    NgaySinh: str = Query(None),
    GioiTinh: int = Query(None),
    QuocTich: str = Query(None),
    DienThoai: str = Query(None),
    SoTaiKhoanToChuc: str = Query(None),
    NgayMoTaiKhoan: str = Query(None),
    TrangThaiTaiKhoan: int = Query(None),
    DiaChiMAC: str = Query(None),
    SO_IMEI: str = Query(None),
    NghiNgo: int = Query(None),
    LyDoCapNhat: str = Query(None),
    UpdateDate: str = Query(None)
):
    results = search_tktt_tochuc(
        Cif=Cif,
        TenToChuc=TenToChuc,
        SoGiayPhepThanhLap=SoGiayPhepThanhLap,
        LoaiGiayToThanhLapToChuc=LoaiGiayToThanhLapToChuc,
        NgayThanhLap=NgayThanhLap,
        DiaChiToChuc=DiaChiToChuc,
        HoTenNguoiDaiDien=HoTenNguoiDaiDien,
        SoGiayToTuyThan=SoGiayToTuyThan,
        LoaiGiayToTuyThan=LoaiGiayToTuyThan,
        NgaySinh=NgaySinh,
        GioiTinh=GioiTinh,
        QuocTich=QuocTich,
        DienThoai=DienThoai,
        SoTaiKhoanToChuc=SoTaiKhoanToChuc,
        NgayMoTaiKhoan=NgayMoTaiKhoan,
        TrangThaiTaiKhoan=TrangThaiTaiKhoan,
        DiaChiMAC=DiaChiMAC,
        SO_IMEI=SO_IMEI,
        NghiNgo=NghiNgo,
        LyDoCapNhat=LyDoCapNhat,
        UpdateDate=UpdateDate
    )
    return {"results": results}

@router.get("/stats")
def stats_page(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})

@router.get("/stats-data")
def stats_data():
    rows = search_tktt_tochuc()
    # Tổng số tổ chức (theo Cif duy nhất)
    orgs = {}
    for r in rows:
        orgs[r.get('Cif')] = r.get('TenToChuc')
    total_orgs = len(orgs)
    # Chú thích trạng thái tài khoản
    status_labels = {
        1: "Đang hoạt động",
        5: "Đã đóng tài khoản"
        # Có thể bổ sung thêm các trạng thái khác nếu cần
    }
    # Thống kê theo trạng thái tài khoản
    status = {}
    for r in rows:
        k = r.get('TrangThaiTaiKhoan')
        status[k] = status.get(k, 0) + 1
    # Thống kê theo năm thành lập
    year = {}
    for r in rows:
        ngay = r.get('NgayThanhLap')
        y = None
        if ngay:
            parts = str(ngay).split('/')
            if len(parts) == 3:
                y = parts[2]
            elif len(parts) == 1 and len(parts[0]) == 4:
                y = parts[0]
        if y:
            year[y] = year.get(y, 0) + 1
    # Thống kê theo năm mở tài khoản
    open_year = {}
    for r in rows:
        ngay = r.get('NgayMoTaiKhoan')
        y = None
        if ngay:
            parts = str(ngay).split('/')
            if len(parts) == 3:
                y = parts[2]
            elif len(parts) == 1 and len(parts[0]) == 4:
                y = parts[0]
        if y:
            open_year[y] = open_year.get(y, 0) + 1
    # Top 10 tổ chức có nhiều tài khoản nhất
    org_acc = {}
    for r in rows:
        cif = r.get('Cif')
        ten = r.get('TenToChuc')
        if cif:
            if cif not in org_acc:
                org_acc[cif] = {'Cif': cif, 'TenToChuc': ten, 'count': 0}
            org_acc[cif]['count'] += 1
    top_orgs = sorted(org_acc.values(), key=lambda x: -x['count'])[:10]
    # 10 tài khoản mở gần nhất
    def parse_date(s):
        from datetime import datetime
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(str(s), fmt)
            except:
                pass
        return None
    latest_accounts = [r for r in rows if r.get('NgayMoTaiKhoan')]
    latest_accounts = sorted(latest_accounts, key=lambda r: parse_date(r.get('NgayMoTaiKhoan')) or 0, reverse=True)[:10]
    # Chuyển datetime về string cho mọi trường trong dict
    def serialize_row(row):
        for k, v in row.items():
            if isinstance(v, (datetime.datetime, datetime.date)):
                row[k] = v.isoformat()
        return row
    top_orgs = [serialize_row(dict(o)) for o in top_orgs]
    latest_accounts = [serialize_row(dict(a)) for a in latest_accounts]
    return JSONResponse({
        'total_orgs': total_orgs,
        'status': status,
        'status_labels': status_labels,
        'year': year,
        'open_year': open_year,
        'top_orgs': top_orgs,
        'latest_accounts': latest_accounts
    })

@router.get("/stats-charts")
def stats_charts_page(request: Request):
    return templates.TemplateResponse("stats_charts.html", {"request": request})
