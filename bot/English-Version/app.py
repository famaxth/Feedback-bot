# -*- coding: utf-8 -*-

from datetime import datetime

import telebot
from telebot import types

import db
import menu
from config import ADMIN_ID, BOT_TOKEN, CHANNEL_URL


db.init_db()
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


try:
    bot.send_message(
        ADMIN_ID, "<a><pre>The bot is running!</pre></a>", parse_mode='HTML')
except Exception as e:
    print(e)


def send_answer_2(message, user_id, message_id):
    if message.chat.id == ADMIN_ID:
        if message.text == "Stop":
            bot.send_message(ADMIN_ID, "You canceled the action",
                             reply_markup=menu.start_admin)
        else:
            try:
                html_teg = "<a></a>"
                for symbol in html_teg:
                    if symbol in message.text:
                        today = datetime.today()
                        date = today.strftime("%Y-%m-%d")
                        bot.send_message(
                            user_id, f"{message.text}", parse_mode='HTML')
                        bot.send_message(
                            ADMIN_ID, "✅ The message was sent successfully!", reply_markup=menu.start_admin)
                        db.add_answer(date, message_id, user_id)
                        break
                else:
                    today = datetime.today()
                    date = today.strftime("%Y-%m-%d")
                    bot.send_message(user_id, f"{message.text}")
                    bot.send_message(
                        ADMIN_ID, "✅ The message was sent successfully!", reply_markup=menu.start_admin)
                    db.add_answer(date, message_id, user_id)
            except Exception as e:
                print(e)
                bot.send_message(ADMIN_ID, "❌ Error!",
                                 reply_markup=menu.start_admin)


def send_answer_1(message):
    try:
        user_id = int(
            ((str(db.return_user_id(int(message.text)))).replace("(", "")).replace(",)", ""))
        message_id = message.text
        msg = bot.send_message(
            ADMIN_ID, "Send me the answer to the question. You can send it in HTML format.")
        bot.register_next_step_handler(msg, send_answer_2, user_id, message_id)
    except:
        bot.send_message(
            ADMIN_ID, "❌ Error! The message was not found.", reply_markup=menu.start_admin)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    database = list(db.return_users_id())
    if str(message.chat.id) not in str(database):
        if message.chat.id == ADMIN_ID:
            bot.send_message(ADMIN_ID, "Hello! \n\nWrite down your question and we will answer you as soon as possible.\n\nBot was created using @por0vos1k",
                             parse_mode='HTML', reply_markup=menu.start_admin)
            today = datetime.today()
            date = today.strftime("%Y-%m-%d")
            db.add_user(message.from_user.first_name,
                        message.from_user.last_name, date, message.chat.id)
        else:
            bot.send_message(
                message.chat.id, "Hello! \n\nWrite down your question and we will answer you as soon as possible.\n\nBot was created using @por0vos1k", parse_mode='HTML')
            today = datetime.today()
            date = today.strftime("%Y-%m-%d")
            db.add_user(message.from_user.first_name,
                        message.from_user.last_name, date, message.chat.id)
    else:
        if message.chat.id == ADMIN_ID:
            bot.send_message(ADMIN_ID, "Hello! \n\nWrite down your question and we will answer you as soon as possible.\n\nBot was created using @por0vos1k",
                             parse_mode='HTML', reply_markup=menu.start_admin)
        else:
            bot.send_message(
                message.chat.id, "Hello! \n\nWrite down your question and we will answer you as soon as possible.\n\nBot was created using @por0vos1k", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "Close":
            bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['text'])
def receive_message(message):
    if message.chat.id != ADMIN_ID:
        try:
            today = datetime.today()
            date = today.strftime("%Y-%m-%d")
            db.add_message(message.from_user.first_name,
                           message.from_user.last_name, date, message.text, message.chat.id)
            enter_the_text = types.InlineKeyboardMarkup()
            but_1 = types.InlineKeyboardButton(
                text="Ответить", url=f"https://t.me/{message.from_user.username}")
            enter_the_text.row(but_1)
            text = (str(db.return_message_id(message.text))).replace("(", "")
            message_id = text.replace(",)", "")
            msg = bot.send_message(
                ADMIN_ID, f"""<a><b>📩 A new message has been received:</b>\n\n<pre>{message.text}</pre>\n\n<b>🙎‍♂️User Information:</b>\nID: <b>{message.chat.id}</b>\nUsername: <b>{message.from_user.username}</b>\nDate: <b>{date}</b>\nMessage number: <pre>{message_id}</pre></a>""", parse_mode='HTML', reply_markup=enter_the_text)
        except Exception as e:
            print(e)
    else:
        try:
            if message.text == "Answer the question":
                msg = bot.send_message(
                    ADMIN_ID, "Enter the message number:")
                bot.register_next_step_handler(msg, send_answer_1)
            elif message.text == "Statistics":
                users = (((str(db.return_users()).replace(
                    "(", "")).replace(",)", "")).replace("[", "")).replace("]", "")
                messages = (((str(db.return_requests()).replace(
                    "(", "")).replace(",)", "")).replace("[", "")).replace("]", "")
                answers = (((str(db.return_answers()).replace(
                    "(", "")).replace(",)", "")).replace("[", "")).replace("]", "")
                bot.send_message(
                    ADMIN_ID, f"<a>Statistics for @{CHANNEL_URL}:\n\n<b>Users:</b>\nAll users: <b>{users}</b>\n\n<b>Messages:</b>\nAll messages: <b>{messages}</b>\nAnswers: <b>{answers}</b></a>", reply_markup=menu.close, parse_mode='HTML')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.send_message(
    ADMIN_ID, "<a><pre>The bot has finished work!</pre></a>", parse_mode='HTML')
