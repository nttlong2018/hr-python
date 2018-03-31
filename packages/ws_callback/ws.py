import requests
import json

_ws_callback_url=""
def set_url(_url):
    "set url callback"
    global _ws_callback_url
    _ws_callback_url=_url
def call(path,data):
    "call api from edx_app"
    if data!=None:
        x=requests.post(_ws_callback_url, json.dumps({"path": path,
                                                "params":json.dump(data)
                                                }))
        if x.status_code==200:
            return json.loads(x.content)
        else:
            return None
    else:
        x = requests.post(_ws_callback_url, json.dumps({"path": path}))
        if x.status_code == 200:
            return json.loads(x.content)
        else:
            return None



