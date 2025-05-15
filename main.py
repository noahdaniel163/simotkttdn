from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from routes import router
import json as pyjson
import os
from datetime import datetime
from re import search, DOTALL
import pandas as pd
import io
import json

app = FastAPI()
app.include_router(router)

templates = Jinja2Templates(directory="templates")

# Đọc dữ liệu mẫu từ file
SAMPLE_DATA_PATH = os.path.join(os.path.dirname(__file__), 'templates', 'sample_data.json')
if os.path.exists(SAMPLE_DATA_PATH):
    with open(SAMPLE_DATA_PATH, encoding='utf-8') as f:
        sample_data = pyjson.load(f)
else:
    sample_data = {}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "sample_data": sample_data
    })

@app.post("/submit", response_class=HTMLResponse)
def submit(request: Request, simo_code: str = Form(...), payload_text: str = Form(""), payload_file: UploadFile = File(None)):
    if payload_file is not None and payload_file.filename:
        payload = pyjson.load(payload_file.file)
    else:
        try:
            payload = pyjson.loads(payload_text)
        except Exception:
            return templates.TemplateResponse("form.html", {"request": request, "error": "Payload không hợp lệ!", "sample_data": sample_data})
    endpoint = f"/simo_{simo_code}/"
    url = request.url_for("simo_" + simo_code)
    import requests as pyrequests
    try:
        resp = pyrequests.post(str(url), json=payload)
        resp.raise_for_status()
        # Lấy block log gần nhất
        log_file = os.path.join("logs", f"simo_{simo_code}.log.txt")
        log_content = ""
        response_headers = None
        response_body = None
        if os.path.exists(log_file):
            with open(log_file, encoding="utf-8") as f:
                lines = f.read().split("-"*60 + "\n")
                blocks = [block.strip() for block in lines if block.strip()]
                latest_block = None
                latest_time = None
                for block in blocks:
                    if block.startswith("["):
                        try:
                            ts = block.split("]")[0][1:]
                            t = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                            if latest_time is None or t > latest_time:
                                latest_time = t
                                latest_block = block
                        except Exception:
                            continue
                if latest_block:
                    # Trích xuất Response Headers và Response
                    m_headers = search(r"Response Headers:(.*?)\nResponse:", latest_block, DOTALL)
                    m_response = search(r"Response:(.*?)$", latest_block, DOTALL)
                    response_headers = m_headers.group(1).strip() if m_headers else None
                    response_body = m_response.group(1).strip() if m_response else None
        result_html = ""
        if response_headers:
            result_html += f"<b>Response Headers:</b><pre>{response_headers}</pre>"
        if response_body:
            result_html += f"<b>Response:</b><pre>{response_body}</pre>"
        if not result_html:
            result_html = "Không tìm thấy kết quả phù hợp."
        return templates.TemplateResponse("form.html", {"request": request, "result": result_html, "sample_data": sample_data})
    except Exception as e:
        log_file = os.path.join("logs", f"simo_{simo_code}.log.txt")
        log_content = ""
        response_headers = None
        response_body = None
        if os.path.exists(log_file):
            with open(log_file, encoding="utf-8") as f:
                lines = f.read().split("-"*60 + "\n")
                blocks = [block.strip() for block in lines if block.strip()]
                latest_block = None
                latest_time = None
                for block in blocks:
                    if block.startswith("["):
                        try:
                            ts = block.split("]")[0][1:]
                            t = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                            if latest_time is None or t > latest_time:
                                latest_time = t
                                latest_block = block
                        except Exception:
                            continue
                if latest_block:
                    m_headers = search(r"Response Headers:(.*?)\nResponse:", latest_block, DOTALL)
                    m_response = search(r"Response:(.*?)$", latest_block, DOTALL)
                    response_headers = m_headers.group(1).strip() if m_headers else None
                    response_body = m_response.group(1).strip() if m_response else None
        result_html = ""
        if response_headers:
            result_html += f"<b>Response Headers:</b><pre>{response_headers}</pre>"
        if response_body:
            result_html += f"<b>Response:</b><pre>{response_body}</pre>"
        if not result_html:
            result_html = f"Lỗi: {str(e)}"
        return templates.TemplateResponse("form.html", {"request": request, "result": result_html, "sample_data": sample_data})

@app.get("/download-template", response_class=HTMLResponse)
def download_template_form(request: Request):
    # Lấy danh sách mã simo từ sample_data
    simo_codes = list(sample_data.keys())
    return templates.TemplateResponse("download_template.html", {"request": request, "simo_codes": simo_codes})

@app.post("/download-template")
def download_template_post(request: Request, simo_code: str = Form(...)):
    # Lấy các trường cho mã simo
    fields = list(sample_data.get(simo_code, [{}])[0].keys())
    # Tạo file excel tạm với tên đúng định dạng
    file_path = f"template_Simo{simo_code.zfill(3)}.xlsx"
    df = pd.DataFrame(columns=fields)
    df.to_excel(file_path, index=False)
    return FileResponse(file_path, filename=file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.get("/excel-to-json", response_class=HTMLResponse)
def excel_to_json_form(request: Request):
    simo_codes = list(sample_data.keys())
    return templates.TemplateResponse("excel_to_json.html", {"request": request, "simo_codes": simo_codes})

@app.post("/excel-to-json", response_class=HTMLResponse)
def excel_to_json_post(request: Request, simo_code: str = Form(...), excel_file: UploadFile = File(...)):
    # Định nghĩa các trường int cho từng simo_code
    int_fields = ["LoaiGiayToThanhLapToChuc", "LoaiGiayToTuyThan", "GioiTinh", "TrangThaiTaiKhoan"]
    if simo_code in ["002", "003"]:
        int_fields = int_fields + ["NghiNgo"]
    dtype_dict = {col: 'Int64' for col in int_fields}
    df = pd.read_excel(io.BytesIO(excel_file.file.read()), dtype=str, engine='openpyxl')
    for col in int_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype('Int64')
    fields = list(sample_data.get(simo_code, [{}])[0].keys())
    df = df[fields]
    string_fields = ["cif", "SoGiayPhepThanhLap", "SoGiayToTuyThan", "DienThoai"]
    for col in df.columns:
        if col in string_fields:
            df[col] = df[col].apply(lambda x: str(int(x)) if isinstance(x, float) and x.is_integer() else str(x) if not pd.isnull(x) else "")
        elif col not in int_fields:
            df[col] = df[col].astype(str)
    # Đảm bảo NghiNgo là int trong json
    json_data = df.to_dict(orient="records")
    if simo_code in ["002", "003"]:
        for row in json_data:
            if "NghiNgo" in row and pd.notnull(row["NghiNgo"]):
                try:
                    row["NghiNgo"] = int(row["NghiNgo"])
                except Exception:
                    row["NghiNgo"] = None
    json_data_str = json.dumps(json_data, indent=2, ensure_ascii=False)
    json_filename = f"converted_{simo_code}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        f.write(json_data_str)
    return templates.TemplateResponse("excel_to_json.html", {
        "request": request,
        "simo_codes": list(sample_data.keys()),
        "json_data": json_data,
        "json_data_str": json_data_str,
        "selected_simo": simo_code,
        "json_download": json_filename
    })

@app.get("/download-json/{filename}")
def download_json(filename: str):
    return FileResponse(filename, media_type="application/json", filename=filename)

@app.get("/logs", response_class=HTMLResponse)
def logs_view(request: Request, simo_code: str = "001"):
    log_file = os.path.join("logs", f"simo_{simo_code}.log.txt")
    log_content = ""
    if os.path.exists(log_file):
        with open(log_file, encoding="utf-8") as f:
            log_content = f.read()
    return templates.TemplateResponse("form.html", {
        "request": request,
        "log_content": log_content,
        "selected_simo": simo_code
    })
