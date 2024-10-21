import subprocess
import requests
import time
import datetime
import schedule
import configparser

start_time = datetime.time(8, 0)
end_time = datetime.time(17, 0)

config = configparser.ConfigParser()
config.read('config.ini')

TELEGRAM_BOT_TOKEN = config['telegram']['bot_token']
TELEGRAM_CHAT_ID = config['telegram']['chat_id']

def check_updates():
    current_time = datetime.datetime.now().time()
    
    if start_time <= current_time <= end_time:
        result = subprocess.run(['sudo', 'apt', 'update'], capture_output=True, text=True)
        if "packages can be upgraded" in result.stdout:
            
            #send_telegram_message("Varsel fra Oslofjord:\n" + result.stdout.split('\n')[-2])  # Sending the line that contains update info

            upgradeable_files = subprocess.run(['sudo', 'apt', 'upgrade', '-y'], capture_output=True, text=True)

            for line in upgradeable_files.stdout.splitlines():
                if "upgraded," in line or "newly installed, " in line or "additional disk space" in line:
                    upgraded_files = line
            
            send_telegram_message("Varsel fra Oslofjord Pi:\n" + upgraded_files)

    else:
        print("Current time is outside the defined time range.")

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
        
send_telegram_message("Varsel fra Oslofjord:\nVarsling om oppdateringer er aktiv")

if __name__ == "__main__":
    schedule.every().day.at("08:00").do(check_updates)

    while True:
        schedule.run_pending()
        time.sleep(1)
