import requests

SIMO_ENDPOINTS = {
    "001": "https://mgsimotest.sbv.gov.vn/simo/khdn/1.0/upload-bao-cao-danh-sach-tktt-khdn-api",
    "002": "https://mgsimotest.sbv.gov.vn/simo/khdn/1.0/upload-bao-cao-tktt-khdn-nngl-api",
    "003": "https://mgsimotest.sbv.gov.vn/simo/khdn/1.0/upload-bao-cao-cap-nhat-tktt-khdn-nngl-api",
    "004": "https://mgsimotest.sbv.gov.vn/simo/khdn/1.0/upload-bao-cao-cap-nhat-danh-sach-tktt-khdn-api",
}

def check_url(url):
    try:
        resp = requests.options(url, timeout=10)
        code = resp.status_code
        if code in [200, 401, 403, 405]:
            return f"Tồn tại (status {code})"
        elif code == 404:
            return "Không tồn tại (404)"
        else:
            return f"Kết quả khác: {code}"
    except Exception as e:
        return f"Lỗi kết nối: {e}"

def main():
    for simo, url in SIMO_ENDPOINTS.items():
        result = check_url(url)
        print(f"SIMO {simo}: {url}\n  => {result}\n")

if __name__ == "__main__":
    main()
