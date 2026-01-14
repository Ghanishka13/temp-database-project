import schedule
import time
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def sync_task():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running Firebase sync...")
    subprocess.run(["python", "fetch_firebase.py"])

def train_task():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Training model...")
    subprocess.run(["python", "train_model.py"])

def main():
    print("\n" + "="*50)
    print("  AUTO SYNC SCHEDULER STARTED")
    print("="*50)
    print("\nSchedules:")
    print("  • Sync Firebase → Excel/CSV: Every 5 minutes")
    print("  • Train Model: Every 30 minutes")
    print("\nPress Ctrl+C to stop\n")
    
    schedule.every(5).minutes.do(sync_task)
    schedule.every(30).minutes.do(train_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n✅ Scheduler stopped")
