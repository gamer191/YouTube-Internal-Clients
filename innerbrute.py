import os
import sys
import time

import requests

client_versions = open('payloads/client_versions.txt', 'r').readlines()
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

client_name_id = sys.argv[1]
for client_version in client_versions:
    client_version = client_version.replace('\n', '').replace('\r', '')
    if client_version == '':
        continue

    for count,host in enumerate(innertube_hosts):
        
        data = data_template.replace('%videoId%', host['video_id']).replace('%clientName%', str(client_name_id)).replace('%clientVersion%', client_version)

        headers = host['headers'].copy()

        while True:
            try:
                response = requests.post('https://' + host['domain'] + '/youtubei/v1/player?key=' + host['key'], data=data, headers=host['headers'], timeout=5)
            except Exception:
                time.sleep(0.5)
                continue
            if response.status_code in {400, 404}:
                if count == "1"
                    print('ClientId: ' + str(client_name_id) + ' ClientVersion: ' + str(client_version) + ' @ ' + host['domain'] +'Response Code: ' + str(response.status_code))
                break
            print('ClientId: ' + str(client_name_id) + ' ClientVersion: ' + str(client_version) + ' @ ' + host['domain'] +'Response Code: ' + str(response.status_code))
            if response.status_code == 200:
                open("payloads/known_client_versions.txt", "a").write("\r\n" + str(client_version))
                break
            if response.status_code != 502:
                sys.exit(192)
