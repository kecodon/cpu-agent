# agent.py

import json
import threading
import time
import os

from config import XMRIG_PATH
from utils import fetch_config, report_status
from miner_runner import run_miner

def build_miner_command(config):
    cmd = [
        XMRIG_PATH,
        "-a", config["algo"],
        "-o", config["pool"],
        "-u", config["wallet"],
        "-p", config.get("worker_id", "cpu-agent"),
        "--donate-level=0"
    ]
    return cmd

def periodic_report():
    while True:
        status = {
            "status": "running",
            "uptime": time.time()
        }
        report_status(status)
        time.sleep(30)

if __name__ == "__main__":
    config = fetch_config()
    if not config:
        print("❌ Could not fetch miner config. Exiting.")
        exit(1)

    miner_cmd = build_miner_command(config)

    # Bắt đầu luồng gửi trạng thái
    t = threading.Thread(target=periodic_report, daemon=True)
    t.start()

    # Chạy miner
    run_miner(miner_cmd)
