import subprocess
import os
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')

TELEGRAM_BOT_TOKEN = config['telegram']['bot_token']
TELEGRAM_CHAT_ID = config['telegram']['chat_id']
PI_NAME = config['telegram']['pi_name']

server_path = os.path.expanduser('~/github/Oslofjord-homepage/node/')
client_path = os.path.expanduser('~/github/Oslofjord-homepage/')

server_command = ['node', 'server.js']
client_command = ['python3', '-m', 'http.server', '9999']

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

def run_terminal_commands_in_background(command, path):
    process = subprocess.run(command, cwd=path, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process

server_process = run_terminal_commands_in_background(server_command, server_path)

client_process = run_terminal_commands_in_background(client_command, client_path)



server_log, server_err = server_process.communicate()
client_log, client_err = client_process.communicate()

if server_err:
    send_telegram_message(f"Varsel fra: {PI_NAME}\nError, couldn't start the server.\nReason: {server_err.decode('utf-8')}")

if client_err:
    send_telegram_message(f"Varsel fra: {PI_NAME}\nError, couldn't start the client.\nReason: {client_err.decode('utf-8')}")

if not server_err and not client_err:
    send_telegram_message(f"Varsel fra: {PI_NAME}\nOslofjord-homepage startet\nStatus server:\n{server_log.decode('utf-8')}\nStatus client:\n{client_log.decode('utf-8')}")