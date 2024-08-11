import os
import shutil
import sys
import time

import requests

client_number = int(sys.argv[1])
client_versions = open(f'Clients/{client_number:03}.txt', 'r').readlines()
data_template = open('payloads/post_data.txt', 'r').read()

response_directory = f'responses/{client_number:03}'
if os.path.exists(response_directory):
    shutil.rmtree(response_directory)
os.makedirs(response_directory)


for client_version in client_versions:
    client_version = client_version.replace('\n', '').replace('\r', '')
    if client_version == '':
        continue
    if client_number in [3,10,14,18,21,23,28,29,30,38,55,63,74,91]:
        user_agent = f'com.google.android.youtube/{client_version} (Linux; U; Android 12; GB) gzip'
    elif client_number in [5,15,16,19,26,33,39,64,68,101]:
        user_agent = f'com.google.ios.youtube/{client_version} (iPhone6,2; U; CPU iOS 12_5_6 like Mac OS X; en_AU)'
    else:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52'

    innertube_hosts = [
        {
            'number': '1',
            'api': 'www.youtube.com',
            'video_id': '3YW3W5RPV-0',
            'domain': 'www.youtube.com',
            'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
            'headers': {
                'Origin': 'https://www.youtube.com',
                'Referer': 'https://www.youtube.com/',
                'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'User-Agent': user_agent,
            },
        },
        {
            'number': '2',
            'api': 'youtube kids',
            'video_id': '3YW3W5RPV-0',
            'domain': 'www.youtubekids.com',
            'key': 'AIzaSyBbZV_fZ3an51sF-mvs5w37OqqbsTOzwtU',
            'headers': {
                'Origin': 'https://www.youtubekids.com',
                'Referer': 'https://www.youtubekids.com/',
                'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'User-Agent': user_agent,
            },
        },
        {
            'number': '3',
            'api': 'youtube music',
            'video_id': '3YW3W5RPV-0',
            'domain': 'music.youtube.com',
            'key': 'AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30',
            'headers': {
                'Origin': 'https://music.youtube.com',
                'Referer': 'https://music.youtube.com/',
                'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'User-Agent': user_agent,
            },
        },
        {
            'number': '4',
            'api': 'Google Drive',
            'video_id': '3YW3W5RPV-0',
            'domain': 'clients6.google.com',
            'key': 'AIzaSyD_InbmSFufIEps5UAt2NmB_3LvBH3Sz_8',
            'headers': {
                'Origin': 'https://clients6.google.com',
                'Referer': 'https://clients6.google.com/',
                'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'User-Agent': user_agent,
            },
        },
    ]
    for host in innertube_hosts:
        data = data_template.replace('%videoId%', host['video_id']).replace('%clientName%', str(client_number)).replace('%clientVersion%', client_version)

        while True:
            if client_number in [18,19,59,74,76,93] and host["number"] in ['1','3']:
                break
            try:
                response = requests.post(f'https://{host["domain"]}/youtubei/v1/player?key={host["key"]}', data=data, headers=host['headers'], timeout=5)
            except Exception:
                time.sleep(0.5)
                continue
            print(f'ClientId: {client_number} ClientVersion: {client_version} @ {host["api"]}Response Code: {response.status_code}')
            if ("Sign in to confirm you’re not a bot" in str(response.text)) or ("This helps protect our community" in str(response.text)):
                print("Bot detected")
                print(response.text)
                break
            if response.status_code == 200:
                out = open(f'{response_directory}/{client_version} {host["api"]}.json', 'w', encoding='utf-8')
                out.write(response.text)
                out.close()
                break
