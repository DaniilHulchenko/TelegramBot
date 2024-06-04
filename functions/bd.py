import sqlite3 as sq
from datetime import datetime
from foundation import history_cursor as cur, db_history, db_connection
from keyboards import il_main_menu


async def make_storage(state):
    async with state.proxy() as data:
        data['command']=list()
        data['user']=list()
        data['time']=list()

async def add_to_db(message=None,state=None):
    if message != None:
        cur.execute('INSERT INTO command_line_history(chat_id,user,command,time) VALUES(?,?,?,?)',(message.chat.id,message.from_user.username,message.text,datetime.now()))
    else:
        async with state.proxy() as data:
            cur.execute('INSERT INTO command_line_history(chat_id,user,command,time) VALUES(?,?,?,?)',(tuple(data.values())))


async def count(state):
    async with state.proxy() as data:
        res=data['type']
    # print(res)
    sum=0
    with db_connection.cursor() as cur:
        for i in res:
            cur.execute(f'select price from ad_type where Ad_type_id = {i} ')
            sum+=float(cur.fetchall()[0]['price'])
    return str(sum)

async def db_push(message,state):
    async with state.proxy() as data:
        with db_connection.cursor() as cur:
            cur.execute(f"select Costomer_id from customer_info where Costomer_id={message.chat.id}")
            has_already=cur.fetchall()
            if has_already == ():
                cur.execute(f'insert into payment_info values(newid(),{int(data["card_num"])},{int(data["cvv"])});')
                if data['org']==1:
                    cur.execute("select newid();")
                    orgid_id = cur.fetchall()[0]['newid()']
                    cur.execute(f'insert into organization values("{orgid_id}","{data["org_name"]}", "{data["org_desc"]}")')
                    cur.execute(f'insert into customer_info values({message.chat.id},"@{message.from_user.username}","{data["PIB"]}","{data["email"]}","{data["phone_number"]}",(select Payment_id from payment_info where card_number={int(data["card_num"])}),"{orgid_id}");')
                else:
                    cur.execute(f'insert into customer_info values({message.chat.id},"@{message.from_user.username}","{data["PIB"]}","{data["email"]}","{data["phone_number"]}",(select Payment_id from payment_info where card_number={int(data["card_num"])}),Null);')


                cur.execute("select newid();")
                or_dit_id = cur.fetchall()[0]['newid()']
                cur.execute(f'insert into order_details values("{or_dit_id}",{data["sum"]},"{data["ditails"]}");')
                cur.execute("select newid();")
                or_id = cur.fetchall()[0]['newid()']
                cur.execute(f'insert into orders values("{or_id}",{message.chat.id},"{or_dit_id}",now(),0);')

                cur.execute('SET FOREIGN_KEY_CHECKS=0;')
                for i in data['type']:
                    cur.execute(f'insert into list_of_ordered_ad_types(order_details_id,ad_type_id) values("{or_dit_id}",{i});')
                await message.answer(f"Thank you for ordered! Your order number: {or_id}")
            else:
                cur.execute("select newid();")
                or_dit_id = cur.fetchall()[0]['newid()']
                cur.execute(f'insert into order_details values("{or_dit_id}",{data["sum"]},"{data["ditails"]}");')
                cur.execute("select newid();")
                or_id = cur.fetchall()[0]['newid()']
                cur.execute(f'insert into orders values("{or_id}",{has_already[0]["Costomer_id"]},"{or_dit_id}",now(),0);')

                # cur.execute('SET FOREIGN_KEY_CHECKS=0;')
                for i in data['type']:
                    cur.execute(
                        f'insert into list_of_ordered_ad_types(order_details_id , ad_type_id ) values("{or_dit_id}",{i});')
                await message.answer(f"Thank you for ordered! Your order number: {or_id}",reply_markup=il_main_menu)
            db_connection.commit()
