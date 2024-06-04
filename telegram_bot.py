import asyncio
from aiogram.utils import executor
from foundation import dp,bot,set_default_commands
from handlers import admin,client,other,inline
from functions import on_start,on_end
from foundation import db_connection


async def main(dp):
    try:

        client.register_handler_client(dp)
        client.register_inline_handler_client(dp)
        # client_menus.register_handler_menu_client()
        # client_menus.register_inline_handler_menu_client()
        admin.register_handler_admin(dp)
        other.register_handler_other(dp)

        inline.register_inline_handlers(dp)

        await set_default_commands(bot)
        await on_start(dp)
    except Exception as ex:
        print("Something wrong with bot register:\n",ex)
if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=main, on_shutdown=on_end)
    except Exception as ex:
        print("Something wrong with bot:\n", ex)
