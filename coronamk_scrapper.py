#!/usr/bin/env python3
import base64
import requests
import json
import pprint
from datetime import datetime
from collections import Counter

import re

PAGE_SIZE=50


def get_messages(group_id,group_key,start_id):
    json_data=[]
    more_messages = True
    url="https://pg.cdn.viber.com/pgws/get_pg_messages"
    params = {"group_id": group_id, "group_key": group_key, "last_msg_seq_id": start_id}
    while more_messages:
        response = requests.get(url, params=params)
        if response.ok:
            current_data = json.loads(base64.b64decode(response.text))
            if 'msgs' in current_data.keys():
                json_data+=current_data['msgs']
                start_id += PAGE_SIZE
                params["last_msg_seq_id"]=start_id
            else:
                more_messages = False
    new_data = []
    for x in json_data:
        if x not in new_data:
            new_data.append(x)

    with open("all_messages.json", "w", encoding="utf8") as fp:
        json.dump(new_data, fp, ensure_ascii=False, indent=4)
    print(len(new_data))
    print(len(json_data))
    return new_data


def filter_ages(data):
    regex=r'([^\n]*(П|п)очина[^\n]*)'
    year_regex = r'([0-9]{2,3}) ?(г|год|и)'
    data_ar = []
    for msg in data:
        if "txt" in msg.keys():
            result = re.findall(regex, msg["txt"])
            if len(result) != 0:
                text = ''.join([x[0] for x in result])
                date = datetime.fromtimestamp(int(msg['date'])/1000)
                years = [int(x[0]) for x in re.findall(year_regex, text)]
                data_ar.append({"date": str(date), "txt": text, "years": years})
            else:
                #data_ar.append({"NOTPARSED": msg})
                pass
        else:
            #data_ar.append({"NOTXT": msg})
            pass

    with open('by_day_ages.json', 'w',  encoding='utf8') as fp:
        json.dump(data_ar, fp, ensure_ascii=False, indent=4)
    return data_ar

def make_csv(filtered):
    years = [y for ys in filtered for y in ys["years"]]
    years = Counter(years)
    str_csv = "Возраст,Број\n"
    for key, val in years.items():
        str_csv += f"{key},{val}\n"
    with open("by_age.csv", "w") as f:
        f.write(str_csv)

if __name__ == "__main__":
    data = get_messages(5432196035989771382,"op3n4ccesst0ken", 0)
    filtered = filter_ages(data)
    make_csv(filtered)
