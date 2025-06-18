# utils.py

import requests
from config import SERVER_URL, WORKER_ID

def fetch_config():
    try:
        url = f"{SERVER_URL}/api/config?worker={WORKER_ID}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return res.json()
        else:
            print(f"⚠️ Failed to get config: {res.status_code}")
    except Exception as e:
        print(f"❌ Error contacting server: {e}")
    return None

def report_status(status: dict):
    try:
        url = f"{SERVER_URL}/api/status"
        data = {
            "worker": WORKER_ID,
            **status
        }
        requests.post(url, json=data, timeout=5)
    except:
        pass  # im lặng nếu gửi lỗi
