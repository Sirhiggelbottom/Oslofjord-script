import psutil
import requests
import time
import configparser

# Threshold settings
CPU_TEMP_THRESHOLD = 70  # degrees Celsius
CPU_USAGE_THRESHOLD = 80  # percent
MEMORY_USAGE_THRESHOLD = 80  # percent
DURATION_THRESHOLD = 60  # seconds

config = configparser.ConfigParser()
config.read('config.ini')

TELEGRAM_BOT_TOKEN = config['telegram']['bot_token']
TELEGRAM_CHAT_ID = config['telegram']['chat_id']
PI_NAME = config['telegram']['pi_name']

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

def check_conditions():
    start_time = None

    while True:
        cpu_temp_data = psutil.sensors_temperatures().get('cpu_thermal')
        if cpu_temp_data:
            cpu_temp = cpu_temp_data[0].current
           
        else:
            return
        
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        if (cpu_temp > CPU_TEMP_THRESHOLD or
            cpu_usage > CPU_USAGE_THRESHOLD or
            memory_usage > MEMORY_USAGE_THRESHOLD):

            if start_time is None:
                start_time = time.time()  # start timer

            elif (time.time() - start_time) >= DURATION_THRESHOLD:
                message = f"Varsel fra {PI_NAME}:\n CPU Temp: {cpu_temp}C,\n CPU Forbruk: {cpu_usage}%,\n Memory Forbruk: {memory_usage}%"
                send_telegram_message(message)
                start_time = None  # reset timer
        else:
            start_time = None  # reset timer

        time.sleep(1)  # Check every second
        
send_telegram_message(f"Varsel fra {PI_NAME}:\nTemperatur / forbruk overvåkning aktiv")    

if __name__ == "__main__":
    check_conditions()