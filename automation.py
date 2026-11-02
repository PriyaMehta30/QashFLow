import schedule
import time
from datetime import datetime
import report

def automated_daily_backup():
    print(f"\n[AUTOMATION] Running daily backup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    success = report.export_to_csv("daily_backup.csv")
    if success:
        print("[AUTOMATION] ✅ Backup successful: daily_backup.csv")
    else:
        print("[AUTOMATION] ❌ Backup failed or no data.")

# Schedule the task to run every day at 20:00 (8:00 PM)
schedule.every().day.at("20:00").do(automated_daily_backup)

# Also schedule it to run every 1 minute just so you can test/see it working for your project demo
schedule.every(1).minutes.do(automated_daily_backup)

print("🤖 Automation Engine Started. Waiting for scheduled tasks...")
print("(Press Ctrl+C to stop)")

while True:
    schedule.run_pending()
    time.sleep(1)