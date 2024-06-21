import os
import sys
import time

import requests

client_number = sys.argv[1]
client_versions = open(f'Clients/{client_number}.txt', 'r').readlines()
data_template = open('payloads/post_data.txt', 'r').read()

innertube_hosts = [
    {
        'video_id': 'vJz8QzO1VzQ',
        'domain': 'www.youtube.com',
        'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'headers': {
            'Origin': 'https://www.youtube.com',
            'Referer': 'https://www.youtube.com/',
            'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52',
        },
    },
    {
        'video_id': 'pckuS--UlV4',
        'domain': 'www.youtubekids.com',
        'key': 'AIzaSyBbZV_fZ3an51sF-mvs5w37OqqbsTOzwtU',
        'headers': {
            'Origin': 'https://www.youtubekids.com',
            'Referer': 'https://www.youtubekids.com/',
            'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52',
        },
    },
    {
        'video_id': 'RY607kB2QiU',
        'domain': 'music.youtube.com',
        'key': 'AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30',
        'headers': {
            'Origin': 'https://music.youtube.com',
            'Referer': 'https://music.youtube.com/',
            'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52',
        },
    },
    {
        'video_id': 'zv9NimPx3Es',
        'domain': 'music.youtube.com',
        'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'headers': {
            'Origin': 'https://music.youtube.com',
            'Referer': 'https://music.youtube.com/',
            'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52',
        },
    },
]

if not os.path.exists('responses'):
    os.makedirs('responses')

requests_failed = 0

for client_version in client_versions:
    client_version = client_version.replace('\n', '').replace('\r', '')
    if client_version == '':
        continue

    for host in innertube_hosts:
        
        data = data_template.replace('%videoId%', host['video_id']).replace('%clientName%', str(client_number)).replace('%clientVersion%', client_version)

        headers = host['headers'].copy()

        while True:
            try:
                response = requests.post(f'https://{host["domain"]}/youtubei/v1/player?key={host["key"]}', data=data, headers=host['headers'], timeout=5)
            except Exception:
                time.sleep(0.5)
                continue
            print(f'ClientId: {client_number} ClientVersion: {client_version} @ {host['domain']}Response Code: {response.status_code})
            if response.status_code in {400, 404}:
                break
            if response.status_code == 200:
                open(client_number, 'a').write(f'{client_version} host: {host["domain"]}\r\n')
                break
            if response.status_code != 502:
                sys.exit(192)
