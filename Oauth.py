import config as cfg
from config import tt_app_key, local_url, tt_app_secret
import random
import string
import requests

def link_gen():
    key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    link = f"https://www.tiktok.com/v2/auth/authorize/?client_key={tt_app_key}&response_type=code&scope=user.info.basic,video.publish,video.upload&redirect_uri={local_url}&state={key}"
    print(link)

def exchange_code_for_token(key, secret, code, Rurl):
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    data = {
        "client_key": key,
        "client_secret": secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": Rurl,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
    else:
        error_response = response.json()
        print("Error:", error_response)
    cfg.ACCESS_TKN = access_token
    cfg.REFRESH_TKN = refresh_token

def exchanger(code):
    exchange_code_for_token(tt_app_key, tt_app_secret, code, local_url)