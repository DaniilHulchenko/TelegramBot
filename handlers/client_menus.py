from typing import Text

from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup

from foundation import db_connection
from keyboards import il_client_order_manager, in_client_start_order, kb_admin
from keyboards.client_kb import il_client_accaunt_manager, il_client_accaunt_manager_add_org, il_main_menu


class FMSClient(StatesGroup):pass

async def main_menu(message):
    await message.answer('Main menu', reply_markup=il_main_menu)

async def my_orders(message):
    await message.answer("Your orders:")
    id=message.chat.id
    with db_connection.cursor() as cur:
        cur.execute('select ord.Order_id,cost.pib,cost.email,ord.order_date, ord_det.total_cost, ord_det.additional_order_information from customer_info as cost inner '
                            'join  orders  as ord on ord.customer_id = cost.Costomer_id '
                            'join order_details as ord_det on ord.order_detail_id=ord_det.order_detail_id '
                            f'where cost.Costomer_id = {id};')
        res=cur.fetchall()
        if res!=():
            # pprint(res)
            for i in res:
                cur.execute('select ad_type.type  from ad_type inner '
                            'join list_of_ordered_ad_types as lor on lor.ad_type_id=ad_type.Ad_type_id '
                            f'where lor.order_details_id=(select order_detail_id from orders where Order_id="{i["Order_id"]}");')
                i['list of ordered types']=[g['type'] for g in cur.fetchall()]
                temp=''
                for g in i:
                    temp+=g+': '+str(i[g])+'\n'
                await message.answer(temp,reply_markup=il_client_order_manager)
        else:
            await message.answer('You dont have orders yet, make first order!',reply_markup=in_client_start_order)

async def ord_manager(call):
    ord_id = call.message.text[:call.message.text.find("\n") + 1].split()[1]
    with db_connection.cursor() as cur:
        cur.execute(f' delete from order_details where order_detail_id=(select order_detail_id from orders where Order_id="{ord_id}") ')
    db_connection.commit()
    await call.message.delete()

async def my_accaunt(message):

    await message.answer("Your accaunt:",reply_markup=kb_admin)
    with db_connection.cursor() as cur:
        cur.execute(f'select * from customer_info where Costomer_id = {message.chat.id} ')
        info = cur.fetchall()
        print(info)
        if info!=():
            await FMSClient.edit_accaunt.set()
            info=info[0]
            await message.answer('Costomer id: '+str(info['Costomer_id']))
            await message.answer('PIB: '+info['pib'],reply_markup=il_client_accaunt_manager)
            await message.answer('Email: '+info['email'],reply_markup=il_client_accaunt_manager)
            await message.answer('Phone number: '+str(info['phone_number']),reply_markup=il_client_accaunt_manager)

            cur.execute(f"select card_number from payment_info where Payment_id = (select payment_info from customer_info where Costomer_id= {message.chat.id})")
            await message.answer('Payment info:  **** **** **** '+str(cur.fetchall()[0]['card_number']%10000),reply_markup=il_client_accaunt_manager)

            if info['Organization_id'] != None:
                cur.execute(f'select Name_of_org from organization where Organization_id="{info["Organization_id"]}"')
                await message.answer('Organization name: '+str(cur.fetchall()[0]['Name_of_org']),reply_markup=il_client_accaunt_manager)
            else:
                await message.answer('Do you wanna add organization to your accaunt ?',reply_markup=il_client_accaunt_manager_add_org)
        else:
            await message.answer('You dont have accaunt yet, make first order for registration!',reply_markup=in_client_start_order)

async def edit_accaunt(call,state):
    edit_item=call.message.text[:call.message.text.find(':')]
    print(edit_item)
    if edit_item=="Payment info":
        await call.message.answer(f'Enter your card number: ')
        await FMSClient.confirm_cand_num.set()
    elif edit_item=='Organization name' or call.message.text=='Do you wanna add organization to your accaunt ?':
        await FMSClient.confirm_org_name.set()
        await call.message.answer(f'Enter your organization name: ')
    elif edit_item=='Email':
        await FMSClient.confirm_email.set()
        async with state.proxy() as data: data["edit_item"]='email'
        await call.message.answer(f'Enter your email: ')
    else:
        async with state.proxy() as data:
            data['edit_item']=str( "".join(list(map(lambda x: '_' if x == " " else x, edit_item.lower()))) )
            # pprint(data['edit_item'])
        await call.message.answer(f'Enter your {edit_item}: ')
        await FMSClient.edit_accaunt_push.set()

async def edit_accaunt_push(message,state,castom=None):
    with db_connection.cursor() as cur:
        if castom == None:
            async with state.proxy() as data:
                    cur.execute(f'update customer_info set {data["edit_item"]}="{message.text}" where Costomer_id = {message.chat.id} ')
        elif 'card_num' in castom:
                 cur.execute(f'update payment_info set card_number={castom["card_num"]} where Payment_id = (select payment_info from customer_info where Costomer_id= {message.chat.id}) ')
                 cur.execute(f'update payment_info set cvv={castom["cvv"]} where Payment_id = (select payment_info from customer_info where Costomer_id= {message.chat.id})')
        elif 'org_name' in castom:
            cur.execute(f'select Organization_id from customer_info where Costomer_id= {message.chat.id}')
            org_id=cur.fetchall()[0]['Organization_id']
            if org_id!=None:
                cur.execute(f'update organization set Name_of_org="{castom["org_name"]}" where Organization_id ="{org_id}"')
                cur.execute(f'update organization set description="{castom["org_desc"]}" where Organization_id ="{org_id})"')
            else:
                cur.execute("select newid();")
                orgid_id = cur.fetchall()[0]['newid()']
                cur.execute(f'insert into organization values("{orgid_id}","{castom["org_name"]}", "{castom["org_desc"]}")')
                cur.execute(f'update customer_info set Organization_id="{orgid_id}" where Costomer_id= {message.chat.id}')
        db_connection.commit()
    await state.finish()
    await my_accaunt(message)


# def register_handler_menu_client(dp: Dispatcher):
#     dp.register_message_handler(my_orders,commands='show_my_orders')
#
#     dp.register_message_handler(my_accaunt, commands='show_my_accaunt')
#     dp.register_message_handler(edit_accaunt_push, state=FMSClient.edit_accaunt_push)
#
# def register_inline_handler_menu_client(dp: Dispatcher):
#     dp.register_callback_query_handler(ord_manager, Text(startswith="ord_"))
#     dp.register_callback_query_handler(edit_accaunt, text='edit_accaunt',state=FMSClient.edit_accaunt)
