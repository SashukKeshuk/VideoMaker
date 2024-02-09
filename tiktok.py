import requests
import json
import config as cfg
import os
import math
import threading
import time
from auth import refresh_access_token

def initialize_video_post(access_token, video_path, video_size, chunk_size, total_chunk_count):
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data = {
        'post_info': {
            'title': 'Nutson test',
            'privacy_level': 'SELF_ONLY',
            'disable_duet': False,
            'disable_comment': False,
            'disable_stitch': False,
            "video_cover_timestamp_ms": 1000
        },
        'source_info': {
            'source': 'FILE_UPLOAD',
            'video_size': video_size,
            'chunk_size': chunk_size,
            'total_chunk_count': total_chunk_count
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def upload_video_chunk(upload_url, video_path, start_byte, end_byte, total_size):
    headers = {
        'Content-Type': 'video/mp4',
        'Content-Length': str(end_byte - start_byte + 1),
        'Content-Range': f'bytes {start_byte}-{end_byte}/{total_size}'
    }
    with open(video_path, 'rb') as f:
        f.seek(start_byte)
        data = f.read(end_byte - start_byte + 1)

    response = requests.put(upload_url, headers=headers, data=data)
    return response

def calculate_chunk_details(file_path):
    file_size = os.path.getsize(file_path)
    chunk_size = min(file_size, 10*1024*1024)  # 10 MB
    total_chunks = math.ceil(file_size / chunk_size)
    return file_size, chunk_size, total_chunks

def finalize_video_post(access_token, publish_id):
    url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data = {
        'publish_id': publish_id
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        return response.json()
    except json.JSONDecodeError:
        print("Статус ответа:", response.status_code)
        print("Тело ответа:", response.text)
        return None
def upload_video_direct(video_path):
    refresh_access_token()
    access_token = cfg.ACCESS_TKN
    video_size, chunk_size, total_chunk_count = calculate_chunk_details(video_path)
    init_response = initialize_video_post(access_token, video_path, video_size, chunk_size, total_chunk_count)
    if 'data' in init_response and 'upload_url' in init_response['data']:
        upload_url = init_response['data']['upload_url']
        publish_id = init_response['data']['publish_id']
        for i in range(total_chunk_count):
            start_byte = i * chunk_size
            end_byte = min(start_byte + chunk_size - 1, video_size - 1)
            upload_response = upload_video_chunk(upload_url, video_path, start_byte, end_byte, video_size)
            if (upload_response.status_code != 200 and upload_response.status_code != 201):
                print("Ошибка загрузки части:", upload_response.text)
        finalize_response = finalize_video_post(access_token, publish_id)
        return finalize_response['error']
    else:
        return 'fail'


#res = upload_video_direct("vid.mp4")