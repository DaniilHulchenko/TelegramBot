from foundation import db_connection, db_history, dp, admin_id

from keyboards import kb_admin,il_admin
from keyboards import kb_client
from keyboards.client_kb import il_main_menu


# from bot_creator import dp,storage
from functions import add_to_db,make_storage
from datetime import datetime
################################################################################################

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text


class FMSAdmin(StatesGroup):
    commands=State()
    # b=State()
    # c=State()
    # d=State()

# @dp.message_handler(commands=['command_line'], state=None)
async def commands_start(message):  #message:type.message / m
    if message.chat.id==admin_id:
        try:
            await FMSAdmin.commands.set()
            # await make_storage()
            await message.answer(f'Enter command:',reply_markup=il_admin)

        except Exception as ex:
            await message.answer(f"Something wrong:\n{ex}")
    else:
        await message.answer("Sorry you are not an admin",reply_markup=il_main_menu)

# @dp.message_handler(state="*", commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def commands_cancel(message, state):
    if await state.get_state() is None:
        await message.answer('Is nothing to cansel')
        return
    # async with state.proxy() as data:
    #     print(data)
    db_history.commit()
    db_connection.commit()
    await state.finish()
    await message.answer("OK!")

# @dp.message_handler(state=FMSAdmin.commands)
async def commands_exe(message, state:FSMContext):
    from functions import ppprint
    try:
        async with state.proxy() as data:
            data['chat_id']=message.chat.id
            data['user']=message.from_user.username
            data['command']=message.text
            data['time']=datetime.now()
            # if 'command' in data:
            #     data['command'].append(message.text)
            #     data['user'].append(message.from_user.name)
            #     data['time'].append(datetime.now())
            # else:
            #     data['command']=list()
            #     data['command'].append(message.text)
            #     data['user']=list()
            #     data['user'].append(message.from_user.name)
            #     data['time']=list()
            #     data['time'].append(datetime.now())
        await add_to_db(state=state)

        with db_connection.cursor() as cursor:
            cursor.execute(message.text)
            res=cursor.fetchall()
            if res != ():
                await message.answer(ppprint(res),reply_markup=kb_admin)
            else:
                await message.answer("Done!",reply_markup=kb_admin)
    except Exception as ex:
        await message.answer(f"Something wrong a1:\n{ex}",reply_markup=kb_admin)
    finally:
        # await state.finish()
        db_connection.commit()

def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['command_line'])

    dp.register_message_handler(commands_cancel, state="*", commands='cancel')
    dp.register_message_handler(commands_cancel, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(commands_exe, state=FMSAdmin.commands)

################################################################################################3