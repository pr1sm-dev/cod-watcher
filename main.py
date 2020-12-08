import requests
import os
import time
import json
import datetime
import logging
import sys

logging.basicConfig(
    filename='cod.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
URL = 'https://673763436741.com/_next/static/chunks/pages/index-11b42ad60ed5bf02081d.js'


def get_page(url=URL):
    r = requests.get(URL)
    return r.text


def post_to_webhook(webhook_url, before_size, after_size):
    webhook_data = {
        "content": "@everyone",
        "embeds": [{
            "title": "Backend Change Detected!",
            "url": "https://673763436741.com/_next/static/chunks/pages/index-11b42ad60ed5bf02081d.js",
            "color": 0,
            "timestamp": str(datetime.datetime.utcnow()),
            "footer": {
                "icon_url": "https://i.imgur.com/Z6jzj2A.png",
                "text": "673763436741"
            },
            "author": {
                "name": "673763436741",
                "url": "https://673763436741.com/",
                "icon_url": "https://i.imgur.com/Z6jzj2A.pngo"
            },
            "fields": [
                {
                    "name": "Previous Size",
                    "value": before_size,
                    "inline": True
                },
                {
                    "name": "New Size",
                    "value": after_size,
                    "inline": True
                }
            ]
        }]
    }

    headers = {'Content-Type': 'application/json'}
    r = requests.post(webhook_url, headers=headers, data=json.dumps(webhook_data))
    print(r.text)


def run():
    if not os.path.isfile('config.json'):
        print('COULD NOT FIND config.json!')
        return

    with open('config.json', 'r') as f:
        webhook_url = json.load(f)['webhook_url']

    file_data = ""
    if os.path.isfile('./data.js'):
        with open('data.js', 'r') as f:
            file_data = f.read()

    while True:
        data = get_page()
        if file_data != data:
            post_to_webhook(webhook_url, len(file_data), len(data))
            logging.debug(f'Differing files: {len(file_data)} -> {len(data)}')
            print(f'Differing files: {len(file_data)} -> {len(data)}')
            file_data = data

            with open('data.js', 'w') as f:
                f.write(file_data)
        else:
            logging.debug(f'Files are the same!')
            print('Files are the same!')

        time.sleep(3)


if __name__ == "__main__":
    run()
