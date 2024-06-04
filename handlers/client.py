from pprint import pprint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from validate_email import validate_email
from functions import count, ppprint

# from handlers.client_menus import *
from keyboards import il_client_type, in_client_start, in_client_start_order, \
    il_client_type_confirmation, il_client_org_confirmation, il_client_order_manager, kb_admin

from foundation import bot, db_connection, dp
from functions import db_push
from keyboards.client_kb import il_client_accaunt_manager, il_client_accaunt_manager_add_org, il_main_menu


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_sticker(chat_id=message.chat.id,
                           sticker="CAACAgIAAxkBAAEGSt1jYt0w2ukP-ILMWISfkyYJC9DrOwACNAEAAlKJkSMTzddv9RwHWCoE")
    await message.answer(f'Hello <b>{message.from_user.username}</b>', parse_mode="html")
    await message.answer("Hello, I'm your assistant for ordering advertising!🤖\n"
                         "What would you like to do ?", reply_markup=in_client_start)


async def main_menu(message):
    await message.answer('Main menu', reply_markup=il_main_menu)


async def call_main_menu(call, state):
    content = " ".join(call.data.split("_")[1:])
    if content == 'make order':
        await make_order(call.message)
    if content == 'show my orders':
        await my_orders(call.message)
    if content == 'show my accaunt':
        await my_accaunt(call.message)


class FMSClient(StatesGroup):
    type_selection = State()
    confirm_PIB = State()
    confirm_ph_number = State()
    confirm_email = State()
    confirm_org = State()
    confirm_cand_num = State()
    confirm_cvv = State()
    ditails = State()

    confirm_org_name = State()
    confirm_org_desc = State()

    edit_accaunt = State()
    edit_accaunt_ = State()
    edit_accaunt_push = State()


async def commands_cancel(message, state):
    if await state.get_state() is None:
        await message.answer('OK', reply_markup=il_main_menu)
        # await message.answer('Is nothing to cansel', reply_markup=il_main_menu)
        # reply_markup=types.ReplyKeyboardRemove()
        return
    async with state.proxy() as data:
        print(data)
    await state.finish()
    await message.answer("You close the dialog window!", reply_markup=il_main_menu)
    # ,reply_markup=types.ReplyKeyboardRemove()


# @dp.register_callback_query_handler(Text(startswith="start_"),state=None)
async def il_start(call):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id - 2)
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
        await bot.delete_message(call.from_user.id, call.message.message_id)
        if call.data == "start_make_order":
            await FMSClient.type_selection.set()
            msg = await call.message.answer("Please indicate which type of advertising you are interested in:",
                                            reply_markup=il_client_type)
            # await bot.sti(call.from_user.id, msg["message_id"] - 2)

        else:
            await call.message.answer("I am your online assistant in choosing and ordering advertising,"
                                      " you can order several types of advertising "
                                      "from me and describe your requirements, then apply for advertising,"
                                      " our operators will consider the application as quickly as possible"
                                      " and help you with everything you need", reply_markup=in_client_start_order)
        await call.answer()
    except Exception as ex:
        # await call.message.answer(ex)
        await  bot.delete_message(call.from_user.id, call.message.message_id)
        await FMSClient.type_selection.set()
        await call.message.answer("Please indicate which type of advertising you are interested in:",
                                  reply_markup=il_client_type)


async def make_order(message):
    await FMSClient.type_selection.set()
    await message.answer("Please indicate which type of advertising you are interested in:",
                         reply_markup=il_client_type)


# Text(startswith='type_')
# @dp.callback_query_handler(text=['Contextual'],state=None)
async def il_type(call, state):
    try:
        content = " ".join(call.data.split('_')[1:])
        if content == 'confirm':
            await call.message.edit_reply_markup()
            await call.message.answer("Good! ☝ its your order list")
            sum = await count(state)
            async with state.proxy() as data:
                data['sum'] = sum
            await call.message.answer("Approximately price:" + sum)
            with db_connection.cursor() as cur:
                cur.execute(f"select Costomer_id from customer_info where Costomer_id={call.message.chat.id}")
                if cur.fetchall() == ():
                    await FMSClient.next()
                    await call.message.answer("Now enter your PIB:")
                else:
                    await FMSClient.ditails.set()
                    await call.message.answer("Do you want to add comment to your order ?")
            return
        if content == 'drop orders':
            async with state.proxy() as data:
                data['type'].clear()
            await bot.delete_message(call.from_user.id, call.message.message_id)
        if content == '?':
            await bot.delete_message(call.from_user.id, call.message.message_id)
            with db_connection.cursor() as cur:
                cur.execute('select * from ad_type;')
                message: str = ''
                for i in cur.fetchall():
                    message += f"Type: \t<b>{i['type']}</b>, Efficiency:\t<b>{i['efficiency']}</b>/5, Price:\t<b>{i['price']}</b>\n"
                await call.message.answer(message, parse_mode="html", reply_markup=il_client_type)
        else:
            # await bot.delete_message(call.from_user.id, call.message.message_id)
            with db_connection.cursor() as cur:
                cur.execute(f"select * from ad_type where type='{content}';")
                res = cur.fetchall()
            async with state.proxy() as data:
                if 'type' not in list(data):
                    data['type'] = list()
                    data['type'].append(res[0]['Ad_type_id'])
                else:
                    if res[0]['Ad_type_id'] not in data['type']:
                        data['type'].append((res[0]['Ad_type_id']))
                    else:
                        await call.answer("This type of ad alredy in you orders!")
                        return

            orders = '<b>Your orders:</b>\n'
            with db_connection.cursor() as cursor:
                for i in data['type']:
                    cursor.execute(f'select type from ad_type where Ad_type_id = {i}')
                    orders += cursor.fetchall()[0]['type'] + "\n"
            msg = await call.message.answer(orders, parse_mode="html", reply_markup=il_client_type_confirmation)
            if len(data['type']) > 1: await bot.delete_message(call.from_user.id, msg["message_id"] - 1)
            await call.answer()

        # async with state.proxy() as data:pass
    except Exception as ex:
        pass
    # await call.message.answer(ex)


async def confirmation_name(message, state):
    async with state.proxy() as data:
        data['PIB'] = message.text
    await FMSClient.next()
    await message.answer("Enter your phone number: ")


async def confirmation_ph_num(message, state):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await FMSClient.next()
    await message.answer("Enter your email: ")


async def confirmaton_email(message, state):
    if validate_email(message.text, verify=True):
        async with state.proxy() as data:
            if 'phone_number' not in data:
                await edit_accaunt_push(message, state)
                # await state.finish()
                await message.delete()
                return
            data['email'] = message.text
            await FMSClient.next()
            await message.answer("Are you from soneone organization?", reply_markup=il_client_org_confirmation)

    else:
        await message.answer('You enter invalid email')


async def confirmation_org(call, state):
    content = call.data.split("_")[1]
    if content == 'no':
        async with state.proxy() as data:
            data['org'] = 0
        await FMSClient.next()
        await call.message.answer("OK!")
        await call.message.answer("Good! Now enter your cand number: ")
    else:
        async with state.proxy() as data:
            data['org'] = 1
        await FMSClient.confirm_org_name.set()
        await call.message.answer("Enter your organization name:")


async def confirmation_org_name(message, state):
    async with state.proxy() as data:
        data['org_name'] = message.text
    await message.answer("Give a litle description of you organization:")
    await FMSClient.confirm_org_desc.set()


async def confirmation_org_description(message, state):
    async with state.proxy() as data:
        data['org_desc'] = message.text
        if "email" not in data:
            await state.finish()
            await edit_accaunt_push(message, state, castom=data)
            return
    await FMSClient.confirm_cand_num.set()
    await message.answer("OK!")
    await message.answer("Good! Now enter your cand number: ")


async def confirm_payment(message, state):
    num = message.text.replace(' ', '')
    with db_connection.cursor() as cur:
        cur.execute('select Payment_id from payment_info where card_number = "{num}"')
        used = cur.fetchall()
    if len(num) == 16 and used == ():
        async with state.proxy() as data:
            data['card_num'] = num
        await message.delete()
        await FMSClient.next()
        await message.answer("Enter cvv:")
    else:
        await message.delete()
        await message.answer("You enter wrong card num")


async def confirm_cvv(message, state):
    if len(message.text) == 3:
        async with state.proxy() as data:
            data['cvv'] = message.text
            if "email" not in data:
                await state.finish()
                await edit_accaunt_push(message, state, castom=data)
                await message.delete()
                return
        await message.delete()
        await message.answer("Do you want to add comment to your order ?")
        await FMSClient.next()
    else:
        await message.delete()
        await message.answer("You enter wrong cvv")


async def ditails(message, state):
    async with state.proxy() as data:
        data['ditails'] = message.text
    await db_push(message, state)
    await state.finish()


async def my_orders(message):
    await message.answer("Your orders:", reply_markup=kb_admin)
    id = message.chat.id
    with db_connection.cursor() as cur:
        cur.execute(
            'select ord.Order_id,cost.pib,cost.email,ord.order_date, ord_det.total_cost, ord_det.additional_order_information from customer_info as cost inner '
            'join  orders  as ord on ord.customer_id = cost.Costomer_id '
            'join order_details as ord_det on ord.order_detail_id=ord_det.order_detail_id '
            f'where cost.Costomer_id = {id};')
        res = cur.fetchall()
        if res != ():
            # pprint(res)
            for i in res:
                cur.execute('select ad_type.type  from ad_type inner '
                            'join list_of_ordered_ad_types as lor on lor.ad_type_id=ad_type.Ad_type_id '
                            f'where lor.order_details_id=(select order_detail_id from orders where Order_id="{i["Order_id"]}");')
                i['list of ordered types'] = [g['type'] for g in cur.fetchall()]
                temp = ''
                for g in i:
                    temp += g + ': ' + str(i[g]) + '\n'
                await message.answer(temp, reply_markup=il_client_order_manager)
        else:
            await message.answer('You dont have orders yet, make first order!', reply_markup=in_client_start_order)


async def ord_manager(call):
    ord_id = call.message.text[:call.message.text.find("\n") + 1].split()[1]
    with db_connection.cursor() as cur:
        cur.execute(
            f' delete from order_details where order_detail_id=(select order_detail_id from orders where Order_id="{ord_id}") ')
    db_connection.commit()
    await call.message.delete()


async def my_accaunt(message):
    await message.answer("Your accaunt:", reply_markup=kb_admin)
    with db_connection.cursor() as cur:
        cur.execute(f'select * from customer_info where Costomer_id = {message.chat.id} ')
        info = cur.fetchall()
        print(info)
        if info != ():
            await FMSClient.edit_accaunt.set()
            info = info[0]
            await message.answer('Costomer id: ' + str(info['Costomer_id']))
            await message.answer('PIB: ' + info['pib'], reply_markup=il_client_accaunt_manager)
            await message.answer('Email: ' + info['email'], reply_markup=il_client_accaunt_manager)
            await message.answer('Phone number: ' + str(info['phone_number']), reply_markup=il_client_accaunt_manager)

            cur.execute(
                f"select card_number from payment_info where Payment_id = (select payment_info from customer_info where Costomer_id= {message.chat.id})")
            await message.answer('Payment info:  **** **** **** ' + str(cur.fetchall()[0]['card_number'] % 10000),
                                 reply_markup=il_client_accaunt_manager)

            if info['Organization_id'] != None:
                cur.execute(f'select Name_of_org from organization where Organization_id="{info["Organization_id"]}"')
                await message.answer('Organization name: ' + str(cur.fetchall()[0]['Name_of_org']),
                                     reply_markup=il_client_accaunt_manager)
            else:
                await message.answer('Do you wanna add organization to your accaunt ?',
                                     reply_markup=il_client_accaunt_manager_add_org)
        else:
            await message.answer('You dont have accaunt yet, make first order for registration!',
                                 reply_markup=in_client_start_order)


async def edit_accaunt(call, state):
    edit_item = call.message.text[:call.message.text.find(':')]
    print(edit_item)
    if edit_item == "Payment info":
        await call.message.answer(f'Enter your card number: ')
        await FMSClient.confirm_cand_num.set()
    elif edit_item == 'Organization name' or call.message.text == 'Do you wanna add organization to your accaunt ?':
        await FMSClient.confirm_org_name.set()
        await call.message.answer(f'Enter your organization name: ')
    elif edit_item == 'Email':
        await FMSClient.confirm_email.set()
        async with state.proxy() as data:
            data["edit_item"] = 'email'
        await call.message.answer(f'Enter your email: ')
    else:
        async with state.proxy() as data:
            data['edit_item'] = str("".join(list(map(lambda x: '_' if x == " " else x, edit_item.lower()))))
            # pprint(data['edit_item'])
        await call.message.answer(f'Enter your {edit_item}: ')
        await FMSClient.edit_accaunt_push.set()


async def edit_accaunt_push(message, state, castom=None):
    with db_connection.cursor() as cur:
        if castom == None:
            async with state.proxy() as data:
                cur.execute(
                    f'update customer_info set {data["edit_item"]}="{message.text}" where Costomer_id = {message.chat.id} ')
        elif 'card_num' in castom:
            cur.execute(
                f'update payment_info set card_number={castom["card_num"]} where Payment_id = (select payment_info from customer_info where Costomer_id= {message.chat.id}) ')
            cur.execute(
                f'update payment_info set cvv={castom["cvv"]} where Payment_id = (select payment_info from customer_info where Costomer_id= {message.chat.id})')
        elif 'org_name' in castom:
            cur.execute(f'select Organization_id from customer_info where Costomer_id= {message.chat.id}')
            org_id = cur.fetchall()[0]['Organization_id']
            if org_id != None:
                cur.execute(
                    f'update organization set Name_of_org="{castom["org_name"]}" where Organization_id ="{org_id}"')
                cur.execute(
                    f'update organization set description="{castom["org_desc"]}" where Organization_id ="{org_id})"')
            else:
                cur.execute("select newid();")
                orgid_id = cur.fetchall()[0]['newid()']
                cur.execute(
                    f'insert into organization values("{orgid_id}","{castom["org_name"]}", "{castom["org_desc"]}")')
                cur.execute(
                    f'update customer_info set Organization_id="{orgid_id}" where Costomer_id= {message.chat.id}')
        db_connection.commit()
    await state.finish()
    await my_accaunt(message)


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(main_menu, commands='main_menu')  # ,state=FMSClient.main_menu

    dp.register_message_handler(start, commands=['start', 'hello'])
    dp.register_message_handler(make_order, commands='make_order')

    dp.register_message_handler(my_orders, commands='show_my_orders')

    dp.register_message_handler(my_accaunt, commands='show_my_accaunt')
    dp.register_message_handler(edit_accaunt_push, state=FMSClient.edit_accaunt_push)

    dp.register_message_handler(commands_cancel, state="*", commands='cancel')
    dp.register_message_handler(commands_cancel, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(confirmation_name, state=FMSClient.confirm_PIB)
    dp.register_message_handler(confirmation_ph_num, state=FMSClient.confirm_ph_number)
    dp.register_message_handler(confirmaton_email, state=FMSClient.confirm_email)
    dp.register_message_handler(confirmation_org_name, state=FMSClient.confirm_org_name)
    dp.register_message_handler(confirmation_org_description, state=FMSClient.confirm_org_desc)
    dp.register_message_handler(confirm_payment, state=FMSClient.confirm_cand_num)
    dp.register_message_handler(confirm_cvv, state=FMSClient.confirm_cvv)
    dp.register_message_handler(ditails, state=FMSClient.ditails)


def register_inline_handler_client(dp: Dispatcher):
    dp.register_callback_query_handler(il_start, Text(startswith="start_"), state=None)
    dp.register_callback_query_handler(call_main_menu, Text(startswith="main_"), state=None)
    dp.register_callback_query_handler(il_type, Text(startswith='type_'), state=FMSClient.type_selection)
    dp.register_callback_query_handler(confirmation_org, Text(startswith="org_"), state=FMSClient.confirm_org)
    dp.register_callback_query_handler(ord_manager, Text(startswith="ord_"))
    dp.register_callback_query_handler(edit_accaunt, text='edit_accaunt', state=FMSClient.edit_accaunt)




