import base64
import requests
from config import USERNAME, PASSWORD, CONSUMER_KEY, CONSUMER_SECRET, TOKEN_URL
import os
import json
from datetime import datetime as dt

def get_sbv_token():
    try:
        auth_string = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "password",
            "username": USERNAME,
            "password": PASSWORD
        }
        response = requests.post(TOKEN_URL, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        token = response.json().get("access_token")
        # Ghi log token
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "token.log.txt")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S')}] TOKEN: {token}\n")
            f.write(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}\n")
            f.write("-"*60 + "\n")
        return token
    except requests.RequestException as e:
        # Ghi log lỗi lấy token
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "token.log.txt")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S')}] TOKEN ERROR: {str(e)}\n")
            f.write("-"*60 + "\n")
        return None
