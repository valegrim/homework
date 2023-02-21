#!/usr/bin/python3
import os.path
import re

LOG="events.log"
PATTERN = re.compile('\[(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}):.+\s(OK|NOK)')

events_nok = {}
if not os.path.isfile(LOG):
    print(f"File '{LOG}' does not exist.")
else:
    with open(LOG) as f:
        content = f.readlines()
    for line in content:
        if (match := PATTERN.match(line)) is not None:
            date, time, status = match.groups()
            if(status == "NOK"):
                if events_nok.get(date) is None: events_nok[date] = {time: 0}
                if events_nok[date].get(time) is None: events_nok[date] |= {time: 0}
                events_nok[date][time] += 1
print(events_nok)
