import requests
import json

def get_server_status(serverURL, serverPort):
    url = "https://mcapi.us/server/status?ip="+serverURL+"&port="+serverPort
    try:
        r = requests.get(url)
        if r.status_code == 200:
            response = json.loads(r.text)
            return response
        else:
            return False
    except:
        return False