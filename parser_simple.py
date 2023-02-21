#!/usr/bin/python3
import re

LOG="events.log"
PATTERN = re.compile('\[\d{4}-\d{2}-\d{2}\s+\d{2}:(\d{2}):.+\s(OK|NOK)')

events_nok = dict()
with open(LOG) as f:
    content = f.readlines()
    for line in content:
        if (match := PATTERN.match(line)) is not None:
            time, status = match.groups()
            if(status == "NOK"):
                events_nok[time] = 1 if events_nok.get(time) is None else events_nok[time] + 1
print(events_nok)
