import requests
import uuid
import threading
import random
import yaml

CONFIG_FILE = "config.yml"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)

def get_proxies():
    proxies_file = load_config().get("proxies_file", "")
    with open(proxies_file, "r") as file:
        return file.read().splitlines()

def get_proxy():
    proxies = get_proxies()
    return random.choice(proxies)

def append_token_to_file(token):
    if token:
        truncated_token = token[41:65]
        print(f"[+] ey...{truncated_token}...")
        with open(load_config().get("output_file", "output.txt"), 'a') as token_file:
            token_file.write(f'https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n')

def make_request():
    while True:
        parent_user_id = str(uuid.uuid4())
        payload = {"partnerUserId": parent_user_id}
        proxy = get_proxy()
        data = {}

        try:
            config = load_config()
            url = config.get("url", "")
            headers = config.get("headers", {})
            response = requests.post(url, json=payload, headers=headers, proxies={"http": proxy, "https": proxy})
            data = response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")

        token = data.get('token')
        append_token_to_file(token)

num_threads = load_config().get("num_threads", 5)

threads = [threading.Thread(target=make_request) for _ in range(num_threads)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
