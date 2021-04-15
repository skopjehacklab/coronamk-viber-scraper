import requests
import base64
import json

VIBER_PUBLIC_GROUP_URL = "https://pg.cdn.viber.com/pgws/get_pg_messages"
VIBER_GET_INFO_URL = "https://pg.cdn.viber.com/pgws/get_info_discover"
VIBER_PUBLIC_GROUP_ID = "5432196035989771382" # "Коронавирус МК Koronavirus"
VIBER_PUBLIC_GROUP_TOKEN = "op3n4ccesst0ken"
VIBER_INVITE_ID = "AQAopiALaleJhEtjCYM/OoPTeFLG4qXUriyvsAsT8K5jFiORNcASU32/rO6IpHCf"

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'})

# start collecting messages from 0, stop when the seq id returned is less that the one requested
def get_all_messages(group_id, group_key, start_id=0):
    params = {"group_id": group_id, "group_key": group_key, "last_msg_seq_id": start_id, "bulk_only": 1, "version": 51}
    while True:
        response = session.get(VIBER_PUBLIC_GROUP_URL, params=params)
        if not response.ok:
            response.raise_for_status()
        if response.headers.get('x-viber-base64') == 'YES':
            text = base64.b64decode(response.text)
        else:
            text = response.text
        data = json.loads(text)
        if data["result"] != 0: # what is this?
            return
        msgs = data.get("msgs")
        if not msgs: # no more messages
            return
        last_seq = max(map(lambda m: m['seq'], msgs))
        if last_seq < params["last_msg_seq_id"]:
            return
        yield from msgs
        params["last_msg_seq_id"] = last_seq + 1


# start collection message from last message, downwards. messages are in reverse order
def get_all_messages_reverse(group_id, group_key, last_id):
    params = {"group_id": group_id, "group_key": group_key, "last_msg_seq_id": last_id, "version": 51}
    while True:
        if params["last_msg_seq_id"] <= 0:
            return
        response = session.get(VIBER_PUBLIC_GROUP_URL, params=params)
        if not response.ok:
            response.raise_for_status()
        if response.headers.get('x-viber-base64') == 'YES':
            text = base64.b64decode(response.text)
        else:
            text = response.text
        data = json.loads(text)
        if data["result"] != 0: # what is this?
            return
        msgs = data.get("msgs")
        if not msgs: # no more messages
            return
        yield from reversed(msgs)
        first_seq = min(map(lambda m: m['seq'], msgs))
        if first_seq <= 1:
            return
        params["last_msg_seq_id"] = first_seq - 1



def get_last_message_id(group_id, invite_link):
    response = session.get(VIBER_GET_INFO_URL, params={"inviteLink": invite_link})
    if not response.ok:
        response.raise_for_status()
    data = response.json()
    return data['communities'][group_id]['group']['lstMsgId']
