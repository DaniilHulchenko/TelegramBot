from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

b1=KeyboardButton('show tables;')
b2=KeyboardButton('/cancel')

kb_admin=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
# kb_admin.add(b1).add(b2)
# kb_admin.insert(b1)
kb_admin.insert(b2)


il_admin=InlineKeyboardMarkup()
il_b1=InlineKeyboardButton(text="Show tables",callback_data='show_tables')
il_admin.add(il_b1)


