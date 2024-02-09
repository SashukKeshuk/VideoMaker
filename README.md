# Video Maker Bot

Это телеграм бот, в котором можно создать видео просто введя тему видео, выбрав язык и продолжительность. Бот по запросу с помощью нейросетей по api создаст видео по заданной теме с помощью нейросетей
ChatGPT4 - текст сценария видео на выбранно языке по теме для видео  -  Есть API
ElevenLabs - многоязычная нейросеть озвучивающая текст (созданный в GPT сценарий)  -  Есть API
Pictory AI - нейросеть, подбирающая по тексту сценария подходящие видеоассоциации и собирающая эо в видеоряд  -  Нету API => нейросеть парсится

После того как бот получит по запросу все эти ресурсы, он наложит аудио на видеоряд, скоррекстировав все по длинне и громкости автоматически, добавит водяной знак и отправит пользователю в чат в качестве ответа на его запрос с темой.
После пользователь может выбрать соц сеть / платформу из базы данных бота, в которую бот опубликует видео (на данный момент поддерживаются youtube, instagram и tiktok).
В текущей версии бот поддерживает 6 языков - английский, русский, испанский, индийский и арабский.
Пример созданного ботом видео - example.mp4
Скриншоты взаимодействия пользователя с ботом - scr1/2.../.png

В дальнейшем планируется внедрение бота в сферы производств и последующая его коммерциализация.
