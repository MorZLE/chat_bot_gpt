import openai
import sqlite3 as sl
from DB import DB
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from prettytable import from_db_cursor
from back import keep_alive
from flask import Flask
from flask import request
from threading import Thread
import time
import requests






def main():
    with open('key.txt', encoding='utf-8') as f:
        key_i = f.readline().rstrip()
        key_tg = f.readline().rstrip()
        admin_id = int(f.readline().rstrip())

    openai.api_key = key_i
    bot = Bot(token=key_tg)
    dp = Dispatcher(bot)
    db = DB()
    db.con_db_app()

    async def start_bot(_):
        global con, cur
        print('Бот онлайн!')
        con = sl.connect('chyrik.db')
        cur = con.cursor()
        con.commit()

    @dp.message_handler(commands=['start'])
    async def com_start(message: types.Message):
        await message.reply('Привет!')

    @dp.message_handler(commands=['hs'])
    async def history(message: types.Message):
        if message.from_user.id == int(admin_id):
            await message.reply(from_db_cursor(cur.execute('SELECT * FROM USER;')))

    @dp.message_handler(commands=['cl'])
    async def clear_hh(message: types.Message):
        if message.from_user.id == int(admin_id):
            res, _ = db.exec('DELETE FROM USER;')
            await message.reply('Грехи прощены!')

    @dp.message_handler(commands=['ban'])
    async def ban(message: types.Message):
        if message.from_user.id == int(admin_id):
            name = message.text.split()[-1]
            db.exec('INSERT INTO BAN (name,time) values(?,?)', name, message.date)
            await message.reply(f'{name} забанен!')

    @dp.message_handler(commands=['unban'])
    async def unban(message: types.Message):
        if message.from_user.id == int(admin_id):
            user = message.text.split()[-1]
            db.exec(f'DELETE FROM BAN WHERE name=?', user)
            await message.reply(f'{user} разбанен!')

    @dp.message_handler(commands=['unbanall'])
    async def unban(message: types.Message):
        if message.from_user.id == int(admin_id):
            db.exec(f'DELETE FROM BAN')
            await message.reply('Все разбанены!')

    @dp.message_handler(commands=['user'])
    async def unban(message: types.Message):
        if message.from_user.id == int(admin_id):
            await message.reply(from_db_cursor(cur.execute('SELECT * FROM BAN;')))

    @dp.message_handler()
    async def send(message: types.Message):
        name = message.from_user.username
        res = check_ban(name)
        if res:
            await message.reply('Дай-ка подумаю...')
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=message.text,
                temperature=0.9,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=["You:"]
            )
            con.execute('INSERT INTO USER (ID, data,time) values(?,?,?)',
                        (message.from_user.username, message.text, message.date))
            con.commit()
            await message.reply(response['choices'][0]['text'])
        else:
            await message.reply('вас забанили')

    def check_ban(name):
        try:
            res, _ = db.exec('select * from BAN where name=?', name)
        except sl.OperationalError:
            return True
        return len(res) == 0

    executor.start_polling(dp, skip_updates=True, on_startup=start_bot)
