import sys
import time

import requests

client_number = sys.argv[1]
client_versions = open('payloads/all_possible_version_numbers.txt', 'r').readlines()
data_template = open('payloads/post_data.txt', 'r').read()

innertube_hosts = [
    {
        'headers': {
            'Origin': 'https://www.youtube.com',
            'Referer': 'https://www.youtube.com/',
            'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52',
        },
    },
]

for client_version in client_versions:
    client_version = client_version.replace('\n', '').replace('\r', '')
    if client_version == '':
        continue

    for host in innertube_hosts:
        
        data = data_template.replace('%videoId%', 'vJz8QzO1VzQ').replace('%clientName%', str(client_number)).replace('%clientVersion%', client_version)

        while True:
            try:
                response = requests.post('https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8', data=data, headers=host['headers'], timeout=5)
            except Exception:
                print('exception')
                continue
            print(f'clientVersion: {client_version} Count {client_version.count('.')} Truthy {client_version.count('.') == 1}')
            if client_version.count('.') == 1:
                print(f'ClientVersion: {client_version} Response Code: {response.status_code}')
            if response.status_code in {400, 404}:
                break
            if response.status_code != 502:
                print(f'ClientVersion: {client_version} Response Code: {response.status_code}')
                sys.exit(192)
