from aiogram import Bot, Dispatcher, executor
# from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage, BaseStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.dispatcher.filters import state
import asyncio

TOKEN = '5388995192:AAHmZ1t6NfQ3CaZHEo7r375uIAj6euAhoJM'
admin_id = 1778407768

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


async def set_default_commands(bot):
    await bot.set_my_commands(commands=[
        BotCommand('start', "Launch bot "),
        BotCommand('main_menu',"Main menu"),
        BotCommand('make_order', 'Make an order'),
        BotCommand('show_my_orders', 'Show your orders'),
        BotCommand('show_my_accaunt', 'Show your accaunt'),
        BotCommand('cancel', 'Close dialog window'),
        BotCommand('command_line', 'Command line(for admin)')
    ]
    )
