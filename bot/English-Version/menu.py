import telebot
from telebot import types


start_admin = telebot.types.ReplyKeyboardMarkup(True, False)
start_admin.add('Statistics')
start_admin.add('Answer the question')


close = types.InlineKeyboardMarkup()
but_1 = types.InlineKeyboardButton(text="Close", callback_data="Close")
close.row(but_1)
