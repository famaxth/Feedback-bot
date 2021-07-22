import random

import sqlite3


def generator_id():
    number = 1
    numbers = "123456789"
    for n in range(number):
        message_id = ""
        for i in range(8):
            message_id += random.choice(numbers)
        return message_id


def ensure_connection(func):

    def decorator(*args, **kwargs):
        with sqlite3.connect('base.db') as conn:
            result = func(conn, *args, **kwargs)

        return result

    return decorator


@ensure_connection
def init_db(conn, force: bool = False):

    c = conn.cursor()

    if force:
        c.execute("DROP TABLE IF EXISTS users")

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id              INTEGER PRIMARY KEY,
        first_name                   STRING,
        last_name                    STRING,
        date_reg                     STRING,
        user_id                    INTEGER);
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS requests (
        id              INTEGER PRIMARY KEY,
        first_name                   STRING,
        last_name                    STRING,
        date                         STRING,
		message 				 	 STRING,
		message_id 				 	INTEGER,
		user_id					   INTEGER);
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS answers (
        id              INTEGER PRIMARY KEY,
        date                         STRING,
        message_id 				 	INTEGER,
        text                        STRING);
    """)

    conn.commit()


@ensure_connection
def add_user(conn, first_name: str, last_name: str, date_reg: str, user_id):
    c = conn.cursor()

    c.execute("INSERT INTO users (first_name, last_name, date_reg, user_id) VALUES (?, ?, ?, ?)",
              (first_name, last_name, date_reg, user_id))

    conn.commit()


@ensure_connection
def add_answer(conn, date: str, message_id, text: str):
    c = conn.cursor()

    c.execute("INSERT INTO answers (date, message_id, text) VALUES (?, ?, ?)",
              (date, message_id, text))

    conn.commit()


@ensure_connection
def add_message(conn, first_name: str, last_name: str, date: str, message: str, user_id):
    id_database = list(return_messages_id())

    while True:
        message_id = generator_id()
        if message_id not in id_database:
            c = conn.cursor()
            c.execute("INSERT INTO requests (first_name, last_name, date, message, message_id, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                      (first_name, last_name, date, message, message_id, user_id))
            conn.commit()
            break


@ensure_connection
def return_users_id(conn):
    c = conn.cursor()

    c.execute("SELECT user_id FROM users")

    all_results = c.fetchall()

    return all_results


@ensure_connection
def return_user_id(conn, message_id):
    c = conn.cursor()

    c.execute("SELECT user_id FROM requests WHERE message_id = ?", (message_id,))

    all_results = c.fetchone()

    return all_results


@ensure_connection
def return_message(conn, user_id):
    c = conn.cursor()

    c.execute("SELECT message FROM requests WHERE user_id = ?", (user_id,))

    all_results = c.fetchone()

    return all_results


@ensure_connection
def return_message_id(conn, message: str):
    c = conn.cursor()

    c.execute("SELECT message_id FROM requests WHERE message = ?", (message,))

    all_results = c.fetchone()

    return all_results


@ensure_connection
def return_messages_id(conn):
    c = conn.cursor()

    c.execute("SELECT message_id FROM requests")

    all_results = c.fetchall()

    return all_results


@ensure_connection
def return_requests(conn):
    c = conn.cursor()

    c.execute("SELECT COUNT(message_id) FROM requests")

    all_results = c.fetchall()

    return all_results


@ensure_connection
def return_users(conn):
    c = conn.cursor()

    c.execute("SELECT COUNT(user_id) FROM users")

    all_results = c.fetchall()

    return all_results


@ensure_connection
def return_answers(conn):
    c = conn.cursor()

    c.execute("SELECT COUNT(id) FROM answers")

    all_results = c.fetchall()

    return all_results
