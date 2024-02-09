import time
import requests
from Oauth import link_gen
from local_serv import app
import threading
import config as cfg

def refresh_access_token():
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_key": cfg.tt_app_key,
        "client_secret": cfg.tt_app_secret,
        "grant_type": "refresh_token",
        "refresh_token": cfg.REFRESH_TKN
    }
    response = requests.post(url, headers=headers, data=data)
    ans = response.json()
    cfg.ACCESS_TKN = ans['access_token']
    threading.Timer(86350, refresh_access_token).start()

#def start_refresh_thread():
#    threading.Thread(target=refresh_access_token).start()


#link_gen()

def run_app():
    app.run(ssl_context=('cert.pem', 'key.pem'), port=443)

#flask_thread = threading.Thread(target=run_app)
#flask_thread.start()

#time.sleep(20)
#print(cfg.ACCESS_TKN)
#print(cfg.REFRESH_TKN)