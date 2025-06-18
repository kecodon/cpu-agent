# miner_runner.py

import subprocess
import time

def run_miner(miner_cmd):
    while True:
        print("⛏️  Starting miner...")
        try:
            proc = subprocess.Popen(miner_cmd)
            proc.wait()
            print("⚠️  Miner exited. Restarting in 5s...")
        except Exception as e:
            print(f"❌ Error running miner: {e}")
        time.sleep(5)
