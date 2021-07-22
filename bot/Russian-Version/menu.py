import telebot
from telebot import types


start_admin = telebot.types.ReplyKeyboardMarkup(True, False)
start_admin.add('Статистика')
start_admin.add('Ответить на вопрос')


close = types.InlineKeyboardMarkup()
but_1 = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
close.row(but_1)
