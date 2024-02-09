# -*- coding: utf-8 -*-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, web_app_info

confirm_mrkp = InlineKeyboardMarkup()
confirm = InlineKeyboardButton('Устраивает', callback_data='ok')
decline = InlineKeyboardButton('Повторно', callback_data='repeat')
confirm_mrkp.add(confirm).insert(decline)

confirm_mrkp2 = InlineKeyboardMarkup()
confirm2 = InlineKeyboardButton('Устраивает', callback_data='ok2')
decline2 = InlineKeyboardButton('Повторно', callback_data='ok')
confirm_mrkp2.add(confirm2).insert(decline2)

publ_mrkp = InlineKeyboardMarkup()
publ = InlineKeyboardButton('Опубликовать', callback_data='publ')
publ_mrkp.add(publ)

durability_mrkp = InlineKeyboardMarkup()
s15 = InlineKeyboardButton('~15 сек', callback_data='sec15')
s30 = InlineKeyboardButton('~30 сек', callback_data='sec30')
s60 = InlineKeyboardButton('~60 сек', callback_data='sec60')
durability_mrkp.add(s15).insert(s30).insert(s60)

lng_mrkp = InlineKeyboardMarkup()
rus = InlineKeyboardButton('Русский', callback_data='lng_rus')
eng = InlineKeyboardButton('Аглийский', callback_data='lng_eng')
ind = InlineKeyboardButton('Индийский', callback_data='lng_ind')
esp = InlineKeyboardButton('Испанский', callback_data='lng_esp')
ar = InlineKeyboardButton('Арабский', callback_data='lng_ar')
lng_mrkp.add(rus).add(eng).add(ind).add(esp).add(ar)