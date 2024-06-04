import types

from aiogram.dispatcher import FSMContext

from foundation import db_connection


# import telebot
#
# from foundation.connection import db_connection
# bot = telebot.TeleBot('5388995192:AAHmZ1t6NfQ3CaZHEo7r375uIAj6euAhoJM')
#
# @bot.message_handler(commands=['start', 'hello'])
# def start(message):
#     m = f'Hello <b>{message.from_user.username}</b> ! How are you?'
#     bot.send_message(message.chat.id, m, parse_mode='html')
#
#
# @bot.message_handler(commands=['help'])
# def help(message):
#     bot.send_message(message.chat.id, message)
#
# @bot.message_handler(commands=['test'])
# def test(message):
#     with db_connection.cursor() as cursor:
#         msg=bot.message_handler(message.chat.id,"Enter command")
#         bot.register_next_step_handler(msg,comm)
#     # bot.send_document(message.chat.id, 'https://drive.google.com/file/d/1BqWtKnZ72bu408JmgdOYI1dpEIUGmR70/view?usp=sharing')
#
# def comm(message):
#     with db_connection.cursor() as cursor:
#         cursor.execute(message.text)
#         bot.send_message(message.chat.id,cursor.fetchall())
#
# @bot.message_handler()
# def get_user_text(message):
#     if message.text.lower() == "how are you?":
#         bot.send_message(message.chat.id, "I`m fine, and you?")
#     elif message.text.lower() == 'id':
#         bot.send_message(message.chat.id, f'Your id is: {message.from_user.id}')
#     else:
#         bot.send_message(message.chat.id, "Sorry?")
#
#
#
# if __name__=="__main__":
#     bot.polling(none_stop=True)

from aiogram.dispatcher.filters.state import StatesGroup, State
#
# from foundation import dp
#
#
# class FMSMachine(StatesGroup):
#     First = State()
#     Second = State()
#
#
# @dp.message_handler(commands=['Contextual'], state=FMSMachine.First)
# async def start(message, state):
#     await FMSMachine.First.set()
#     await message.answer("Enter First: ")
#
#
# @dp.message_handler(commands=['Contextual'], state=FMSMachine.First)
# async def one(message, state):
#     async with state.proxy() as data:
#         data['first']=message.text
#     await message.answer("Enter Second: ")
#     await FMSMachine.next()
#
#
# @dp.message_handler(commands=['Contextual'], state=FMSMachine.Second)
# async def two(message, state):
#     async with state.proxy() as data:
#         data['second']=message.text
#     await state.finish()

async def add_to_db(message: types.Message ,state: FSMContext):
        with db_connection.cursor() as cur:
            async with state.proxy() as data:
                cur.execute('INSERT INTO table VALUES(?,?,?,?)',(data[1], data[2], data[3], data[4]))
        db_connection.commit()

