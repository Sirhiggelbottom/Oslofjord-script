import subprocess
import time
import datetime
import schedule
import logging

start_time = datetime.time(8, 0)
end_time = datetime.time(17, 0)

log_file = "Update_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

def check_updates():
    current_time = datetime.datetime.now().time()
    
    if start_time <= current_time <= end_time:
        result = subprocess.run(['sudo', 'apt', 'update'], capture_output=True, text=True)
        if "can be upgraded" in result.stdout:

            upgradeable_files = subprocess.run(['sudo', 'apt', 'dist-upgrade', '-y'], capture_output=True, text=True)

            

            for line in upgradeable_files.stdout.splitlines():
                if "upgraded," in line and "newly installed, " in line:
                    upgraded_files = line
                    logging.info(f"Updated Packages: {upgraded_files}")

    else:
        print("Current time is outside the defined time range.")

if __name__ == "__main__":
    check_updates()
    schedule.every().day.at("08:00").do(check_updates)

    while True:
        schedule.run_pending()
        time.sleep(1)
