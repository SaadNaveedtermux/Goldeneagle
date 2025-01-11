import requests
import time
import json
import random
from threading import Thread

# Read authentication tokens from data.txt
with open("data.txt", "r") as file:
    auth_tokens = [line.strip() for line in file if line.strip()]

# API URLs
tap_url = "https://gold-eagle-api.fly.dev/tap"

# Headers template (common for all requests except Authorization)
headers_template = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://telegram.geagle.online",
    "priority": "u=1, i",
    "referer": "https://telegram.geagle.online/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def send_tap_request(auth_token):
    headers = headers_template.copy()
    headers["authorization"] = f"Bearer {auth_token}"

    data = {
        "available_taps": 1000,
        "count": random.randint(270, 310),
        "timestamp": int(time.time()),
        "salt": "83fded5f-fac6-4882-82a6-26723fe8071c"
    }

    try:
        response = requests.post(tap_url, headers=headers, data=json.dumps(data))
        print(f"TAP Response ({auth_token[:10]}...): {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"TAP Request failed for {auth_token[:10]}: {e}")

def process_account(auth_token):
    while True:
        send_tap_request(auth_token)
        time.sleep(2)

# Start a thread for each token
threads = []
for token in auth_tokens:
    thread = Thread(target=process_account, args=(token,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
