import subprocess
import os
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')

TELEGRAM_BOT_TOKEN = config['telegram']['bot_token']
TELEGRAM_CHAT_ID = config['telegram']['chat_id']
PI_NAME = config['telegram']['pi_name']

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

client_path = os.path.expanduser('~/github/Oslofjord-homepage/')
client_command = ['python3', '-m', 'http.server', '9999']

try:

    client_process = subprocess.run(client_command, cwd=client_path, capture_output=True, text=True, check=True)

    result = client_process.stdout
    err = client_process.stderr

except Exception as e:
   print(f"Error: {e}")
