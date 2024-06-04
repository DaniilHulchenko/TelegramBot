from aiogram.dispatcher.filters import Text

from aiogram import types,Dispatcher

from foundation import bot
# from bot_creator import dp
from keyboards import kb_client

# @dp.message_handler()





async def other(message):
    # await bot.answer_callback_query(message.chat.id, "You in order menu- to censel enter /cancel ", show_alert=True)
    await message.delete()



def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(other,state="*")

