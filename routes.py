from fastapi import APIRouter, HTTPException, Response
import datetime
import requests
from auth import get_sbv_token
from config import ENTRYPOINT_URL_001, ENTRYPOINT_URL_002, ENTRYPOINT_URL_003, ENTRYPOINT_URL_004
from models import Simo001Payload, Simo002Payload, Simo003Payload, Simo004Payload
import os
from datetime import datetime as dt
import subprocess

router = APIRouter()

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
