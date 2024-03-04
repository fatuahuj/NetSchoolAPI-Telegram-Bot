import sqlite3
database = sqlite3.connect("bot.sqlite")
cursor = database.cursor()
def add_user(message):
    cursor.execute("SELECT id FROM users WHERE id=?", (message.chat.id,))
    user = cursor.fetchone()
    if user is None:
        cursor.execute("INSERT INTO users VALUES(?,?,?,?)", (message.chat.id, "log", "pass", "school",))
    else:
        return True
def change_info(message):
    cursor.execute("DELETE FROM users WHERE id=?", (message.chat.id,))
    database.commit()
def add_user_log(message):
    cursor.execute("UPDATE users SET login=? WHERE id=?", (message.text, message.chat.id,))
    database.commit()
def add_user_school(message):
    cursor.execute("UPDATE users SET school=? WHERE id=?", (message.text, message.chat.id,))
    database.commit()
def add_user_pass(message):
    cursor.execute("UPDATE users SET password=? WHERE id=?", (message.text, message.chat.id,))
    database.commit()
def get_user_log(user_id):
    cursor.execute("SELECT login FROM users WHERE id=?", (user_id,))
    user_log = cursor.fetchone()[0]
    return user_log
def get_user_pas(user_id):
    cursor.execute("SELECT password FROM users WHERE id=?", (user_id,))
    user_pas = cursor.fetchone()[0]
    return user_pas
def get_user_sch(user_id):
    cursor.execute("SELECT school FROM users WHERE id=?", (user_id,))
    user_sch = cursor.fetchone()[0]
    return user_sch
