#!/usr/bin/python3
import re
import requests
import time

POOL = [
"maria.ru",
"rose.ru",
"sina.ru",
]
INTERVAL = 5

def check_res(res):
    if res.status_code != 200:
        return("Error {}".format(res.status_code))
    try:
        json = res.json()
    except:
        return("Error: Not json")
    if "count" in json:
        return(json["count"])
    else:
        return("Format error")

def write_report(host, data):
    (year, month, day, hour, min, sec) = time.strftime("%Y %m %d %H %M %S").split()
    print(f"{year}-{month}-{day} {hour}:{min}:{sec} {host} {data}")
    return()

timestamp = time.time()
while True:
    for host in POOL:      
        try:
            res = requests.get(f"http://{host}/api/count", timeout=(5))
        except:
            write_report(host, "Connection Error")
            continue
        write_report(host, check_res(res))
    while((time.time() - timestamp) < INTERVAL):
        time.sleep(0.5)
    timestamp = time.time()
