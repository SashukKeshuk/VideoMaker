# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, web_app_info
from pydub import AudioSegment
from pydub.playback import play
from moviepy.editor import VideoFileClip, AudioFileClip
from config import bot_api_token, el_labs_api, OPAI, EX_PATH, DOWN_PATH
import openai
from markups import *
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import glob
import pyperclip
from audiostretchy.stretch import stretch_audio
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import keys
from selenium.common.exceptions import NoSuchElementException
from pydub.utils import which
import requests
import soundfile as sf
from datetime import datetime
from watermark import watermark
from tiktok import upload_video_direct
import re

bot = Bot(token=bot_api_token)
dp = Dispatcher(bot)
openai.api_key = OPAI
CO = webdriver.ChromeOptions()
CO.add_argument("--allow-file-access-from-files")
CO.add_argument("--disable-web-security")
CO.add_argument("--safebrowsing-disable-download-protection")
CO.add_argument('--disable-gpu')
CO.add_argument('--disable-dev-shm-usage')
CO.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=EX_PATH, chrome_options=CO)
path = DOWN_PATH
D, l, LNG, texts, prev_msgs, themes = dict(), dict(), dict(), dict(), dict(), dict()
driver.implicitly_wait(10)
ST = FST = PST = 1

def f1(s):
    print(s)
    S = s.split('|')
    if (len(S) == 1):
        return S[0], S[0]
    else:
        return S[0], S[1]

def load_audio_from_video(video_file):
    video = VideoFileClip(video_file)
    video.audio.write_audiofile("temp_audio.wav")
    return AudioSegment.from_wav("temp_audio.wav")

def SA(target_length, uid):
    song = AudioSegment.from_wav(f'output{uid}.wav')
    length = len(song)
    R = target_length / length
    stretch_audio(f"output{uid}.wav", "stretched_audio.wav", ratio=R)

def mix_audio(audio1, audio2):
    return audio1.overlay(audio2)

def replace_audio(video_file, audio_file, uid):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
    final = video.set_audio(audio)
    final.write_videofile(f"output{uid}.mp4")

def pictory(text):
    global ST
    if (text[0] == ' '):
        text = text[1:]
    pyperclip.copy(text)
    ST = 0
    wait = WebDriverWait(driver, 10000)
    st = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                          '#root > div.full-height > div.page-content.d-flex.align-items-stretch.full-height > div > div.css-chrv4g > div:nth-child(1) > div.jss4.jss1.css-j7qwjs > div.MuiBox-root.css-1xrh4yi > button')))
    st.click()
    time.sleep(5)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                           '#root > div.full-height > div.page-content.d-flex.align-items-stretch.full-height > div > main > div > div > div:nth-child(1) > div > button.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary.MuiButton-sizeMedium.MuiButton-outlinedSizeMedium.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary.MuiButton-sizeMedium.MuiButton-outlinedSizeMedium.css-1hg5b18')))
    element.click()
    time.sleep(5)
    print('element')
    proc = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                        'button.MuiButton-contained:nth-child(2)')))
    proc.click()
    print('proc')
    time.sleep(10)
    temp = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                        '#step-3-fixed-height > div.col-md-60.col-big-xl.col-tb-7.flex-space-between.white-background > div.hide-trimmer-progress.col.p-0.top-scene-section > div > div:nth-child(2) > div > div > div.d-flex.ControlledOpenSelect.MuiBox-root.css-0')))
    temp.click()
    print('temp')
    time.sleep(10)
    form = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                        '#menu- > div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation0.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation8.MuiPopover-paper.css-pf9eht > ul > li:nth-child(2) > div')))
    form.click()

    #time.sleep(50)
    print('here')
    maing = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                         '#generate-button-dropdown > a')))
    print('chosen')
    actions = ActionChains(driver)
    actions.key_down(keys.Keys.CONTROL)
    actions.move_to_element(maing)
    actions.click(maing)
    actions.perform()
    time.sleep(1)
    print('hovered')
    gen = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                       '#btnGenerate')))
    gen.click()

    time.sleep(60)
    download = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                            '.MuiDialogActions-root > div:nth-child(3)')))
    download.click()
    time.sleep(30)
    list_of_files = glob.glob(path + '/*')
    latest_file = max(list_of_files, key=os.path.getmtime)
    driver.get('https://app.pictory.ai/textinput')
    time.sleep(15)
    ST = 1
    return latest_file

async def on_startup(_):
    driver.get('https://app.pictory.ai/textinput')
    print('bot online')

@dp.message_handler(commands=['start'])
@dp.callback_query_handler(text='repeat')
async def start(msg: types.Message):

    print(msg.from_user.id)
    open(f'output{msg.from_user.id}.mp3', 'a').close()
    open(f'output{msg.from_user.id}.mp3', 'w').close()
    await bot.send_message(msg.from_user.id,
                           f'Здравствуйте {msg.from_user.username}, введите тематику видео в именительном падеже. После того, как вы введете сообщение бот возьмет ваше сообщение с создаст видео на эту тему. Что бы прервать процесс генерации видео, либо начать генерировать новое видео, напишите боту \'/start\'. Но перед началом генераации выберите продолжительность видео.',
                           parse_mode='html', reply_markup=durability_mrkp)

@dp.callback_query_handler(text_contains = 'sec')
async def sec(clb: types.CallbackQuery):
    if (clb.data == 'sec15'):
        x = 75
    elif (clb.data == 'sec30'):
        x = 150
    else:
        x = 300
    D[clb.from_user.id] = x
    await bot.send_message(clb.from_user.id, "Отлично! Теперь выберите язык видео.", parse_mode='html', reply_markup=lng_mrkp)

@dp.callback_query_handler(text_contains = 'lng_')
async def lng(clb: types.CallbackQuery):
    if (clb.data == 'lng_rus'):
        LNG[clb.from_user.id] = 'русском'
    elif (clb.data == 'lng_eng'):
        LNG[clb.from_user.id] = 'английском'
    elif (clb.data == 'lng_esp'):
        LNG[clb.from_user.id] = 'испанском'
    elif (clb.data == 'lng_ar'):
        LNG[clb.from_user.id] = 'арабском'
    else:
        LNG[clb.from_user.id] = 'индийском'
    await bot.send_message(clb.from_user.id,
                           f'Отлично! Теперь введите тематику видео в именительном падеже', parse_mode='html')

#@dp.message_handler(text=['x'])
@dp.callback_query_handler(text='ok2')
async def compile(clb: types.CallbackQuery):
    #l[clb.from_user.id] = "C:\\Users\\user\\Downloads\\Bananasaretrulya.mp4"
    print('compile')
    global FST
    if (FST == 0):
        await bot.send_message(clb.from_user.id, f"Ваш запрос на сборку видео поставлен в очередь")
    while (FST == 0):
        time.sleep(3)
    FST = 0
    await bot.send_message(clb.from_user.id, 'Собираем и отправляем вам итоговое видео...')
    print(l[clb.from_user.id])
    audio1b = load_audio_from_video(str(l[clb.from_user.id]))
    audio1 = audio1b - 30
    AudioSegment.from_mp3(f"output{clb.from_user.id}.mp3").export(f"output{clb.from_user.id}.wav", format="wav")
    SA(len(audio1), clb.from_user.id)
    audio2_stretched = AudioSegment.from_wav(f'stretched_audio.wav')
    mixed_audio = mix_audio(audio1, audio2_stretched)
    mixed_audio.export("temp_audio_mixed.wav", format="wav")
    replace_audio(str(l[clb.from_user.id]), "temp_audio_mixed.wav", clb.from_user.id)
    await bot.send_message(clb.from_user.id, 'Все готово, вот итоговое видео!')
    watermark(clb.from_user.id)
    with open(f"output{clb.from_user.id}_f.mp4", 'rb') as vid:
        await bot.send_video(clb.from_user.id, video=vid)
    os.remove(f"output{clb.from_user.id}.wav")
    FST = 1
    await bot.send_message(clb.from_user.id, 'Что бы опубликовать это видео, напишите #<номер тт аккаунта> для публикации. Для генерации нового видео напишите \'/start\'')

@dp.message_handler(text_contains='#')
async def fpubl(clb: types.Message):
    global PST
    while (PST == 0):
        time.sleep(3)
    PST = 0
    nums = str(clb.text)
    nums = nums[1:]
    try:
        num = int(nums)
        try:
            with open(f"output{clb.from_user.id}_f.mp4", 'rb') as vid:
                await bot.send_video(937306169, video=vid)
            upload_video_direct(f"output{clb.from_user.id}_f.mp4")
            time.sleep(180)
            await bot.send_message(clb.from_user.id, "видео успешно опубликовано")
        except:
            await bot.send_message(clb.from_user.id, "не получилось опубликовать видео в тик ток")
    except:
        await bot.send_message(clb.from_user.id, "номер введен некорректно")
    PST = 1

@dp.message_handler()
async def text_audio_gen(msg: types.Message):
    print('audio')
    open(f'output{msg.from_user.id}.mp3', 'w').close()
    print(LNG[msg.from_user.id])
    print(D[msg.from_user.id])
    PR = f"Сгенерируй новый текст БЕЗ РАЗБИЕНИЯ НА АБЗАЦЫ на {LNG[msg.from_user.id]} языке для видео на тему \"{msg.text}\" (текст должен получиться длинной около {D[msg.from_user.id]} символов)";
    if (LNG[msg.from_user.id] != 'английском'):
        PR += "с максимально дословным перевод на английский язык и раздели 2 текста символом |"
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=PR,
        temperature=0.9,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    ans = response['choices'][0]['text']
    ans = str(ans)
    T1, T2 = f1(ans)
    print(T1 + ' ||| ' + T2 + '\n')
    texts[msg.from_user.id] = T2
    themes[msg.from_user.id] = msg.text
    #T1 = T1.replace('.', '. . . . ... ... .. .. . . .')
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": el_labs_api
    }

    data = {
        "text": T1,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open(f'output{msg.from_user.id}.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    with open(f'output{msg.from_user.id}.mp3', 'rb') as audio:
        await bot.send_audio(msg.from_user.id, audio)
        await bot.send_message(msg.from_user.id, 'Аудио устраивает? Если нет, то аудио будет сгенерировано повторно.',
                               reply_markup=confirm_mrkp)

@dp.callback_query_handler(text='ok')
async def vidm(clb: types.CallbackQuery):
    print('video')
    print(texts[clb.from_user.id] + '\n\n\n')
    if (ST == 0):
        await bot.send_message(clb.from_user.id, f"Ваш запрос находится в очереди, пожалуйста, ожидайте...")
    while (ST == 0):
        time.sleep(3)
    await bot.send_message(clb.from_user.id, f"Начинаем генерацию вашего видео, процесс требует времени..")
    l[clb.from_user.id] = pictory(texts[clb.from_user.id])
    print(l[clb.from_user.id])
    with open(l[clb.from_user.id], 'rb') as vid:
        await bot.send_video(clb.from_user.id, video=vid)
    await bot.send_message(clb.from_user.id,
                           'Все готово! Видео устраивает? Если нет, то видео будет сгенерировано повторно.',
                           reply_markup=confirm_mrkp2)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
