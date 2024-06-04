from foundation import bot, db_connection

from datetime import datetime
from foundation import history_cursor as cur,db_history
from handlers.admin import FMSAdmin
from keyboards import kb_admin


# @dp.callback_query_handlers(text="show_tables")
async def sh_tb(message):
    await bot.delete_message(message.from_user.id,message.message.message_id)
    try:
        from functions import ppprint
        with db_connection.cursor() as cursor:
            cursor.execute("show tables;")
            await bot.send_message(message.from_user.id,ppprint(cursor.fetchall()),reply_markup=kb_admin)
        cur.execute('INSERT INTO command_line_history(chat_id,user,command,time) VALUES(?,?,?,?)',(message.from_user.id, message.from_user.username, 'show tables;', datetime.now()))
        db_history.commit()
    except Exception as ex:
        await bot.send_message(message.from_user.id, ex)

def register_inline_handlers(dp):
    dp.register_callback_query_handler(sh_tb,text='show_tables',state=FMSAdmin.commands)