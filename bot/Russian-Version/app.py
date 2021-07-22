from datetime import datetime

import db
import menu
from config import ADMIN_ID, BOT_TOKEN, CHANNEL_URL

import telebot
from telebot import types


db.init_db()
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


try:
    bot.send_message(
        ADMIN_ID, "<a><pre>Бот запущен!</pre></a>", parse_mode='HTML')
except Exception as e:
    print(e)


def send_answer_2(message, user_id, message_id):
    if message.chat.id == ADMIN_ID:
        if message.text == "Отмена":
            bot.send_message(ADMIN_ID, "Вы отменили действие",
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
                            ADMIN_ID, "✅ Сообщение было успешно отправлено!", reply_markup=menu.start_admin)
                        db.add_answer(date, message_id, user_id)
                        break
                else:
                    today = datetime.today()
                    date = today.strftime("%Y-%m-%d")
                    bot.send_message(user_id, f"{message.text}")
                    bot.send_message(
                        ADMIN_ID, "✅ Сообщение было успешно отправлено!", reply_markup=menu.start_admin)
                    db.add_answer(date, message_id, user_id)
            except Exception as e:
                print(e)
                bot.send_message(ADMIN_ID, "❌ Ошибка!",
                                 reply_markup=menu.start_admin)


def send_answer_1(message):
    try:
        user_id = int(
            ((str(db.return_user_id(int(message.text)))).replace("(", "")).replace(",)", ""))
        message_id = message.text
        msg = bot.send_message(
            ADMIN_ID, "Пришлите мне ответ на вопрос. Вы можете отправить его в формате HTML.")
        bot.register_next_step_handler(msg, send_answer_2, user_id, message_id)
    except:
        bot.send_message(
            ADMIN_ID, "❌ Ошибка! Сообщение не было найдено.", reply_markup=menu.start_admin)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    database = list(db.return_users_id())
    if str(message.chat.id) not in str(database):
        if message.chat.id == ADMIN_ID:
            bot.send_message(ADMIN_ID, "Здравствуйте! \n\nНапишите ваш вопрос и мы ответим Вам в ближайшее время.\n\nЭтот бот был создан с помощью @por0vos1k",
                             parse_mode='HTML', reply_markup=menu.start_admin)
            today = datetime.today()
            date = today.strftime("%Y-%m-%d")
            db.add_user(message.from_user.first_name,
                        message.from_user.last_name, date, message.chat.id)
        else:
            bot.send_message(
                message.chat.id, "Здравствуйте! \n\nНапишите ваш вопрос и мы ответим Вам в ближайшее время.\n\nЭтот бот был создан с помощью @por0vos1k", parse_mode='HTML')
            today = datetime.today()
            date = today.strftime("%Y-%m-%d")
            db.add_user(message.from_user.first_name,
                        message.from_user.last_name, date, message.chat.id)
    else:
        if message.chat.id == ADMIN_ID:
            bot.send_message(ADMIN_ID, "Здравствуйте! \n\nНапишите ваш вопрос и мы ответим Вам в ближайшее время.\n\nЭтот бот был создан с помощью @por0vos1k",
                             parse_mode='HTML', reply_markup=menu.start_admin)
        else:
            bot.send_message(
                message.chat.id, "Здравствуйте! \n\nНапишите ваш вопрос и мы ответим Вам в ближайшее время.\n\nЭтот бот был создан с помощью @por0vos1k", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "Закрыть":
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
                ADMIN_ID, f"""<a><b>📩 Получено новое сообщение:</b>\n\n<pre>{message.text}</pre>\n\n<b>🙎‍♂️Информация о пользователе:</b>\nID: <b>{message.chat.id}</b>\nUsername: <b>{message.from_user.username}</b>\nВремя получения: <b>{date}</b>\nНомер сообщения: <pre>{message_id}</pre></a>""", parse_mode='HTML', reply_markup=enter_the_text)
        except Exception as e:
            print(e)
    else:
        try:
            if message.text == "Ответить на вопрос":
                msg = bot.send_message(
                    ADMIN_ID, "Введите номер сообщения:")
                bot.register_next_step_handler(msg, send_answer_1)
            elif message.text == "Статистика":
                users = (((str(db.return_users()).replace(
                    "(", "")).replace(",)", "")).replace("[", "")).replace("]", "")
                messages = (((str(db.return_requests()).replace(
                    "(", "")).replace(",)", "")).replace("[", "")).replace("]", "")
                answers = (((str(db.return_answers()).replace(
                    "(", "")).replace(",)", "")).replace("[", "")).replace("]", "")
                bot.send_message(
                    ADMIN_ID, f"<a>Статистика бота @{CHANNEL_URL}:\n\n<b>Пользователи:</b>\nВсего пользователей: <b>{users}</b>\n\n<b>Сообщения:</b>\nВсего сообщений: <b>{messages}</b>\nОтветов: <b>{answers}</b></a>", reply_markup=menu.close, parse_mode='HTML')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    bot.polling(none_stop=True)


bot.send_message(
    ADMIN_ID, "<a><pre>Бот закончил работу!</pre></a>", parse_mode='HTML')
