from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.chrome.service import Service

import time
from datetime import datetime
import pytz
import os
import random
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.auth.transport.requests
from instagrapi import Client
from config import inst_login, inst_pswd, EX_PATH

moscow_tz = pytz.timezone('Europe/Moscow')
#cl = Client()
#cl.login(inst_login, inst_pswd)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
driver_pub = webdriver.Chrome(executable_path=EX_PATH, options=options)
driver_pub.get('https://lk.smmwix.com/')

def publ_INST(uid):
    try:
        media = cl.video_upload(
            path=f"output{uid}_f.mp4",
            caption="test video",
        )
        return True
    except Exception as e:
        return str(e)


def publ_TT(uid, num) -> bool:
    print('publ')
    res = False
    try:
        wait2 = WebDriverWait(driver_pub, 1000)
        pb = WebDriverWait(driver_pub, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             f'#__next > div > div > div.col-span-12.sm\:col-span-9.md\:col-span-8.lg\:col-span-9 > div:nth-child(3) > div > div:nth-child({num}) > div > button:nth-child(5)')))
        pb.click()
        time.sleep(10)
        upld = wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                           '#__next > div > div > div.col-span-12.sm\:col-span-9.md\:col-span-8.lg\:col-span-9 > div:nth-child(4) > div > div.col-span-12.lg\:col-span-8 > form > input[type=file]')))
        upld.send_keys(f"C:\\users\\user\\Desktop\\OpenServer\\domains\\videomaker\\output{uid}_f.mp4")
        time.sleep(30)
        moscow_time = datetime.now(moscow_tz)
        h = moscow_time.hour
        m = moscow_time.minute
        m += 2
        if (m >= 60):
            m -= 60
            h += 1

        selh = wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                           '#__next > div > div > div.col-span-12.sm\:col-span-9.md\:col-span-8.lg\:col-span-9 > div:nth-child(4) > div > div.col-span-12.lg\:col-span-8 > form > div:nth-child(6) > div > div.col-span-5.lg\:col-span-3.grid.grid-cols-3.gap-3 > div:nth-child(2) > select')))

        select_element = Select(selh)
        select_element.select_by_value(str(h))
        time.sleep(5)
        selm = wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                           '#__next > div > div > div.col-span-12.sm\:col-span-9.md\:col-span-8.lg\:col-span-9 > div:nth-child(4) > div > div.col-span-12.lg\:col-span-8 > form > div:nth-child(6) > div > div.col-span-5.lg\:col-span-3.grid.grid-cols-3.gap-3 > div:nth-child(3) > select')))

        select_element = Select(selm)
        select_element.select_by_value(str(m))
        time.sleep(5)

        finalb = wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                             '#__next > div > div > div.col-span-12.sm\:col-span-9.md\:col-span-8.lg\:col-span-9 > div:nth-child(4) > div > div.col-span-12.lg\:col-span-8 > form > div.flex.items-center.justify-between > button:nth-child(1)')))
        finalb.click()
        time.sleep(20)
        driver_pub.get('https://lk.smmwix.com/')
        time.sleep(20)
        res = True
    except Exception as e:
        print(e)
    finally:
        driver_pub.get('https://lk.smmwix.com/')

def authenticate_with_oauth():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "google_client.json"

    #OAuth 2.0 login
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    return youtube

def upload_video(youtube, file_path):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Test Title",
                "description": "Test Description",
                "tags": ["test", "example"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(file_path)
    )
    response = request.execute()
    print(response)

#youtube = authenticate_with_oauth()

def upload_YT(uid):
    try:
        upload_video(youtube, f"output{uid}_f.mp4")
        return True
    except:
        return False
