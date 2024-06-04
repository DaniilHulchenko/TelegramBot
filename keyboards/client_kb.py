from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/command_line')
kb_client.add(b1)
# kb_client.insert(b1)

il_bar = InlineKeyboardMarkup()
il_but = InlineKeyboardButton(text="YouTube", url="https://www.youtube.com/")
il_bar.add(il_but)

make_order = InlineKeyboardButton("Make an order 💸", callback_data="start_make_order")
in_client_start = InlineKeyboardMarkup(inline_keyboard=[
    [
        make_order,
        InlineKeyboardButton("About me📃", callback_data="start_read_info")
    ]
])
in_client_start_order = InlineKeyboardMarkup(inline_keyboard=[[make_order]])

il_client_type = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Contextual", callback_data='type_Contextual'),
        InlineKeyboardButton(text="Banner🖼", callback_data='type_Banner'),
        InlineKeyboardButton(text="Video📽", callback_data='type_Video'),
    ],
    [
        InlineKeyboardButton(text="In mobile apps📱", callback_data='type_In_mobile apps'),
        InlineKeyboardButton(text="Popup windows💭", callback_data='type_Popup_windows'),
        InlineKeyboardButton(text="Push notifications📌", callback_data='type_Push_notifications')
    ],
    [
        InlineKeyboardButton(text="Newsletters📩", callback_data='type_Newsletters'),
        InlineKeyboardButton(text="Social networks📧", callback_data='type_Social_networks'),
        InlineKeyboardButton(text="Teaser", callback_data='type_Teaser')
    ],
    [
        InlineKeyboardButton(text="I dont know ❓", callback_data='type_?')
    ]
]
)

il_client_type_confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Confirm your order👌", callback_data="type_confirm")
    ],
    [
        InlineKeyboardButton(text="Drop orders❌", callback_data="type_drop_orders")
    ]
])

il_client_org_confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Yes✔", callback_data="org_yes"),
        InlineKeyboardButton(text="No❌", callback_data="org_no")
    ]
])

il_client_order_manager = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Delete❌", callback_data="ord_manager")]
])

il_client_accaunt_manager = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Edit", callback_data="edit_accaunt")
    ]
])
il_client_accaunt_manager_add_org = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕', callback_data='edit_accaunt')]
])

il_main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Make an order 💸', callback_data='main_make_order')
    ],
    [
        InlineKeyboardButton(text='Show my orders 📃', callback_data='main_show_my_orders'),
        InlineKeyboardButton(text=('Show my personal info ℹ'), callback_data='main_show_my_accaunt')
    ]
])
