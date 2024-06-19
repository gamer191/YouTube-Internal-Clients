import requests
import os
import sys
import time

client_versions = open("payloads/client_versions.txt", "r").readlines()
data_template =  open("payloads/post_data.txt", "r").read()

innertube_hosts = [
    {
        "video_id": "vJz8QzO1VzQ", # normal video
        "domain": "www.youtube.com",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
        "headers": {
            "Origin": "https://www.youtube.com",
            "Referer": "https://www.youtube.com/",
            "Accept-Language": "de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52"
        }
    },
    {
        "video_id": "pckuS--UlV4", # video "for kids"
        "domain": "www.youtubekids.com",
        "key": "AIzaSyBbZV_fZ3an51sF-mvs5w37OqqbsTOzwtU",
        "headers": {
            "Origin": "https://www.youtubekids.com",
            "Referer": "https://www.youtubekids.com/",
            "Accept-Language": "de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52"
        }
    },
    {
        "video_id": "RY607kB2QiU", # music video
        "domain": "music.youtube.com",
        "key": "AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30",
        "headers": {
            "Origin": "https://music.youtube.com",
            "Referer": "https://music.youtube.com/",
            "Accept-Language": "de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52"
        }
    },
    {
        "video_id": "zv9NimPx3Es", # another music video
        "domain": "music.youtube.com",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
        "headers": {
            "Origin": "https://music.youtube.com",
            "Referer": "https://music.youtube.com/",
            "Accept-Language": "de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52"
        }
    }
]

if not os.path.exists('responses'):
    os.makedirs('responses')

requests_failed = 0

client_name_id = sys.argv[1]
for counter,client_version in enumerate(client_versions, start=1):
    client_version = client_version.replace("\n", "").replace("\r", "")
    if client_version == "":
        continue

    for i, host in enumerate(innertube_hosts):

        try_id = str(client_name_id) + "_" + client_version + "_" + str(len(innertube_hosts) - i) + "_" + host["domain"] + "_" + host["key"]
        
        data = data_template.replace("%videoId%", host["video_id"]).replace('%clientName%', str(client_name_id)).replace('%clientVersion%', client_version)

        headers = host["headers"].copy()

        for i in range(0, 4):
            while True:
                try:
                    response = requests.post("https://" + host["domain"] + "/youtubei/v1/player?key=" + host["key"], data=data, headers=host["headers"], timeout=5)
    
                    if response.status_code == 400 or response.status_code == 404:
                        break
                    elif response.status_code == 502:
                        print("code 502")
                        continue
                    else:
                        print("Counter: " + str(counter) + "ClientId: " + str(client_name_id) + " ClientVersion: " + str(client_version) + " @ " + host["domain"] +"Response Code: " + str(response.status_code))
                        sys.exit(int(counter) + "1234" + int(response.status_code))
                except Exception as ex:
                    print("request failed")
                    time.sleep(0.5)
                    print(ex)
                    continue
