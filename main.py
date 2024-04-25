import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from netschoolapi import NetSchoolAPI
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from aiogram import F

import gpt
from cfg import add_user, add_user_log, add_user_pass, get_user_log, get_user_pas, change_info, add_user_school, get_user_sch
from gpt import today, week, kb

logging.basicConfig(level=logging.INFO)
bot = Bot(token="YOUR_TOKEN_BOT")
dp = Dispatcher(storage=MemoryStorage())

class user_reg(StatesGroup):
    pas = State()
    login = State()
    school = State()
@dp.message(user_reg.login)
async def add_name_(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await state.clear()
    add_user_log(message)
    sch = [[types.KeyboardButton(text="МОУ СОШ №2")], [types.KeyboardButton(text="МОУ «СОШ № 13»")]]
    school = types.ReplyKeyboardMarkup(keyboard=sch, resize_keyboard=True, input_field_placeholder="Выберите свою школу")
    await bot.send_message(chat_id, "Выберите вашу школу", reply_markup=school)
    await state.set_state(user_reg.school)
@dp.message(user_reg.school)
async def add_school_(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await state.clear()
    add_user_school(message)
    await bot.send_message(chat_id, "Введите пароль от сетевого города",reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(user_reg.pas)
@dp.message(user_reg.pas)
async def add_pas_(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await state.clear()
    add_user_pass(message)
    try:
        ns = NetSchoolAPI('https://sgo.edu-74.ru/')
        await ns.login(f'{get_user_log(chat_id)}', f'{get_user_pas(chat_id)}', f'{get_user_sch(chat_id)}')
        s = await ns.diary()

        if s:

            keyboard = types.ReplyKeyboardMarkup(
                keyboard=gpt.kb,
                resize_keyboard=True,
                input_field_placeholder="Выберите день недели"
            )
            await bot.send_message(chat_id, "Регистрация завершена", reply_markup=keyboard)
    except:
        kb = [
            [
                types.KeyboardButton(text="Изменить данные")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите день недели"
        )
        await bot.send_message(chat_id,f"Похоже данные не верны", reply_markup=keyboard)
        change_info(message)
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_status = add_user(message)
    if user_status == True:
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=gpt.kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите день недели"
        )
        await bot.send_message(chat_id, f"Твой логин: {get_user_log(chat_id)}\nТвой пароль: {get_user_pas(chat_id)}", reply_markup=keyboard)
    else:
        reg =[[types.KeyboardButton(text="Регистрация")]]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=reg,
            resize_keyboard=True,
            input_field_placeholder="Выберите день недели"
        )
        await bot.send_message(chat_id, f"Привет, {message.chat.username}.\nЯ создан, чтобы отправить тебе расписание.\nМой создатель: @Vanusha_in", reply_markup=keyboard)
@dp.message(F.text.lower() == "регистрация")
async def change(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_status = add_user(message)
    if user_status == True:
        user_name = get_user_log(chat_id)
        user_pas = get_user_pas(chat_id)
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=gpt.kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите день недели"
        )
        await bot.send_message(chat_id, f"Привет {user_name}, {user_pas}", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id, f"Введите логин от сетевого города",reply_markup=keyboard)
        await state.set_state(user_reg.login)
@dp.message(F.text.lower() == "изменить данные")
async def change(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_status = add_user(message)
    if user_status == True:
        user_name = get_user_log(chat_id)
        user_pas = get_user_pas(chat_id)
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=gpt.kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите способ подачи"
        )
        await bot.send_message(chat_id, f"Привет {user_name}, {user_pas}", reply_markup=keyboard)
    else:


        await bot.send_message(chat_id, f"Введите логин от сетевого города")
        await state.set_state(user_reg.login)
@dp.message(F.text.lower() == "сегодня")
async def Today(message: types.Message):
    chat_id = message.chat.id
    try:
        ns = NetSchoolAPI('https://sgo.edu-74.ru/')
        await ns.login(
            f'{get_user_log(chat_id)}',  # Логин
            f'{get_user_pas(chat_id)}',  # Пароль
            f'{get_user_sch(chat_id)}',  # Название школы
        )
        s = await ns.diary()
        await ns.logout()
        await bot.send_message(chat_id,f"Сегодня \n{today(s)}")
    except: await bot.send_message(chat_id,"Похоже ты сегодня не учишься")
@dp.message(F.text.lower() == "понедельник")
async def Week(message: types.Message):
    chat_id = message.chat.id
    try:
        ns = NetSchoolAPI('https://sgo.edu-74.ru/')
        await ns.login(
            f'{get_user_log(chat_id)}',  # Логин
            f'{get_user_pas(chat_id)}',  # Пароль
            f'{get_user_sch(chat_id)}',  # Название школы
        )
        s = await ns.diary()
        await ns.logout()
        await bot.send_message(chat_id,f"Понедельник \n{week(s,0)}")
    except:

        await bot.send_message(chat_id,f"Странно ничего нет, наверное сетевой не работает(")
@dp.message(F.text.lower() == "вторник")
async def Week(message: types.Message):
    chat_id = message.chat.id
    try:
        ns = NetSchoolAPI('https://sgo.edu-74.ru/')
        await ns.login(
            f'{get_user_log(chat_id)}',  # Логин
            f'{get_user_pas(chat_id)}',  # Пароль
            f'{get_user_sch(chat_id)}',  # Название школы
        )
        s = await ns.diary()
        await ns.logout()
        await bot.send_message(chat_id,f"Вторник \n{week(s,1)}")
    except:


        await bot.send_message(chat_id,f"Странно ничего нет, наверное сетевой не работает(")
@dp.message(F.text.lower() == "среда")
async def Week(message: types.Message):
    chat_id = message.chat.id
    try:
        ns = NetSchoolAPI('https://sgo.edu-74.ru/')
        await ns.login(
            f'{get_user_log(chat_id)}',  # Логин
            f'{get_user_pas(chat_id)}',  # Пароль
            f'{get_user_sch(chat_id)}',  # Название школы
        )
        s = await ns.diary()
        await ns.logout()
        await bot.send_message(chat_id,f"Понедельник \n{week(s,2)}")
    except:

        await bot.send_message(chat_id, f"Странно ничего нет, наверное сетевой не работает(")
@dp.message(F.text.lower() == "четверг")
async def Week(message: types.Message):
    chat_id = message.chat.id
    try:
        ns = NetSchoolAPI('https://sgo.edu-74.ru/')
        await ns.login(
            f'{get_user_log(chat_id)}',  # Логин
            f'{get_user_pas(chat_id)}',  # Пароль
            f'{get_user_sch(chat_id)}',  # Название школы
        )
        s = await ns.diary()
        await ns.logout()
        await bot.send_message(chat_id,f"Понедельник \n{week(s,3)}")
    except:

        await bot.send_message(chat_id, f"Странно ничего нет, наверное сетевой не работает(")
@dp.message(F.text.lower() == "пятница")
async def Week(message: types.Message):
    chat_id = message.chat.id
    try:
        ns = NetSchoolAPI('https://sgo.edu-74.ru/')
        await ns.login(
            f'{get_user_log(chat_id)}',  # Логин
            f'{get_user_pas(chat_id)}',  # Пароль
            f'{get_user_sch(chat_id)}',  # Название школы
        )
        s = await ns.diary()
        await ns.logout()
        await bot.send_message(chat_id,f"Понедельник \n{week(s,4)}")
    except:

        await bot.send_message(chat_id, f"Странно ничего нет, наверное сетевой не работает(")

@dp.message(F.text.lower() == "помощь")
async def Week(message: types.Message):
    chat_id = message.chat.id
    await  bot.send_message(chat_id,
                            f'Вот список команд:\n'
                                    f'/info - информация о боте\n'
                                    f'/start - показать свои данные'
                                    )
@dp.message(Command("info"))
async def cmd_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id, f'Привет, я @Vanusha_in создал этого бота. \nЕсли возникли проблемы или вопросы пиши.')
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
