#!/usr/bin/python3
import re
import requests
import time
from concurrent.futures import ThreadPoolExecutor

#request interval
INTERVAL = 5
#URL (/ at the end if directory) and metrics
POOL = {
"http://maria.ru/api/count/": ["count"],
"http://rose.ru/api/count/": ["count"],
"http://sina.ru/api/count/": ["count", "cpu"],
}
#number of concurrent thread
THREAD = 10
#connection timeout
TIMEOUT = 5
#print answer delay from server
DELAY = True

def dict_format(json):
    string = False
    for key in json.keys():
        string = string + f", {key} = {json[key]}" if string else f"{key} = {json[key]}"
    return(string)

def check_res(res):
    if res.status_code != 200:
        return("Error {}".format(res.status_code))
    try:
        json = res.json()
    except:
        return("Error: Not json")
    if DELAY is True: json |= {"delay": res.elapsed.total_seconds()}
    for metrica in POOL[res.url]:
        if metrica not in json:
            return("Error: Metrica error")
    return(dict_format(json))

def write_report(host, data):
    (year, month, day, hour, min, sec) = time.strftime("%Y %m %d %H %M %S").split()
    print(f"{year}-{month}-{day} {hour}:{min}:{sec} {host} \t{data}")
    return()

def req_api(url):
    host = re.search(r'^https?:\/\/([\w\.\-]+)\/', url)
    host = host.group(1)
    try:
        res = requests.get(url, timeout=(TIMEOUT))
    except:
        write_report(host, "Error: Connection failed")
        return(False)
    write_report(host, check_res(res))
    return(True)

timestamp = time.time()
while True:
    with ThreadPoolExecutor(max_workers=THREAD) as executor:
        executor.map(req_api, POOL)
    while((time.time() - timestamp) < INTERVAL):
        time.sleep(0.5)
    timestamp = time.time()
