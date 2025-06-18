import requests
import subprocess
import time
import signal
from config import SERVER_URL, WORKER_NAME, XMRIG_PATH

miner_process = None

def fetch_config():
    url = f"{SERVER_URL}/api/config?worker={WORKER_NAME}"
    print(f"📡 Fetching config from {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"❌ Failed to fetch config: {e}")
        return None

def start_miner(config):
    global miner_process
    if miner_process:
        print("🛑 Stopping existing miner...")
        miner_process.terminate()
        miner_process.wait()
        time.sleep(1)

    cmd = [
        XMRIG_PATH,
        "-a", config["algo"],
        "-o", config["pool"],
        "-u", config["wallet"],
        "-p", config["worker"],
        "--threads", str(config["threads"])
    ]
    print("⛏️ Starting miner...")
    miner_process = subprocess.Popen(cmd)

def main():
    while True:
        config = fetch_config()
        if config:
            start_miner(config)
        else:
            print("⚠️ Using existing config (if any).")
        time.sleep(300)  # kiểm tra mỗi 5 phút

def handle_exit(sig, frame):
    global miner_process
    print("\n🛑 Exiting agent...")
    if miner_process:
        miner_process.terminate()
        miner_process.wait()
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    main()
