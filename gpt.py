import datetime
from aiogram import types
from netschoolapi import NetSchoolAPI
ns = NetSchoolAPI('https://sgo.edu-74.ru/')
def week(s, x):
    a = 1
    f = ''
    db = [[], []]
    for i in range(len(s.schedule[x].lessons)):
        d = s.schedule[x].lessons[i].assignments
        db.insert(i, f"{s.schedule[x].lessons[i].subject}\n")
        if len(d) > 0:
            for y in range(len(d)):
                if d[y].mark == None and d[y].type == "Домашнее задание":
                    db[i] += f"{d[y].type}:  {d[y].content}\n"
                elif d[y].mark != None:
                    db[i] += f"{d[y].type}: оценка ({d[y].mark}), {d[y].content}\n"
    db = db[:-2]
    for i in range(len(db)):
        f += f"{db[i]} \n"
    return f

def today(s):
    f = ''
    db = [[], []]
    today = datetime.date.today().weekday()
    for i in range(len(s.schedule[today].lessons)):
        d = s.schedule[today].lessons[i].assignments
        db.insert(i, f"{s.schedule[today].lessons[i].subject}\n")
        if len(d) > 0:
            for y in range(len(d)):
                if d[y].mark == None and d[y].type == "Домашнее задание":
                    db[i] += f"{d[y].type}:  {d[y].content}\n"
                elif d[y].mark != None:
                    db[i] += f"{d[y].type}: оценка ({d[y].mark}), {d[y].content}\n"
    db = db[:-2]
    for i in range(len(db)):
        f += f"{db[i]} \n"
    return f

kb = [
            [
                types.KeyboardButton(text="Сегодня"),
                types.KeyboardButton(text="Понедельник"),
            ],
            [
                types.KeyboardButton(text="Вторник"),
                types.KeyboardButton(text="Среда")
            ],
            [
                types.KeyboardButton(text="Четверг"),
                types.KeyboardButton(text="Пятница")
            ],
            [
                types.KeyboardButton(text="Помощь")
            ]
        ]
