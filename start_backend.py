import subprocess
import os
import configparser
import requests
import time

config = configparser.ConfigParser()
config.read('config.ini')

TELEGRAM_BOT_TOKEN = config['telegram']['bot_token']
TELEGRAM_CHAT_ID = config['telegram']['chat_id']
PI_NAME = config['telegram']['pi_name']


server_path = os.path.expanduser('~/github/Oslofjord-homepage/node/')
server_command = ['node', 'server.js']


def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")


try:

    server_process = subprocess.Popen(server_command, cwd=server_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    time.sleep(2)

    return_code = server_process.poll()

    if return_code is not None:
        err = server_process.stderr.read()
        send_telegram_message(f"Varsel fra {PI_NAME}:\nError, kunne ikke starte Backend server.\nGrunn:{err}")
    else:
        send_telegram_message(f"Varsel fra {PI_NAME}:\nBackend server startet")
    
except Exception as e:
    send_telegram_message(f"Varsel fra: {PI_NAME}\nException, reason:\n {e}")