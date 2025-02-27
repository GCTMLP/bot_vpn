from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from text.keyboard_text import(
    MONTH_1,
    MONTH_2,
    MONTH_3,
    MONTH_6,
    MAIN_MENU,
    PROLONG_ALL,
    NEW_KEY,
    PROLONG_KEY,
    MY_KEYS,
    INSTRUCTION,
    HELP,
    PAY_TEXT,
    TO_PAY
)

def chose_doing_markup():
    inline_kb_list = [
        [InlineKeyboardButton(text=NEW_KEY, callback_data='new')], 
        [InlineKeyboardButton(text=PROLONG_KEY, callback_data='prolong')],
        [InlineKeyboardButton(text=MY_KEYS, callback_data='my_keys')], 
        [InlineKeyboardButton(text=INSTRUCTION, callback_data='instruction')], 
        [InlineKeyboardButton(text=HELP, callback_data='help')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def choose_period_kb():
   inline_kb_list = [
        [InlineKeyboardButton(text=MONTH_1, callback_data='mnth1')], 
        [InlineKeyboardButton(text=MONTH_2, callback_data='mnth2')],
        [InlineKeyboardButton(text=MONTH_3, callback_data='mnth3')], 
        [InlineKeyboardButton(text=MONTH_6, callback_data='mnth6')],
        [InlineKeyboardButton(text=MAIN_MENU, callback_data='cancel')]
   ]
   return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def choose_keys_kb(key_names, selected_keys = []):
    to_pay = False
    inline_kb_list = []
    for name in key_names:
        if name in selected_keys:
            name_text= name+ ' ✅'
            to_pay = True
        else:
            name_text = name
        inline_kb_list.append([InlineKeyboardButton(text=name_text, callback_data=name_text)])
    inline_kb_list.append([InlineKeyboardButton(text=PROLONG_ALL, callback_data='all.ovpn')])
    if to_pay:
        inline_kb_list.append([InlineKeyboardButton(text=TO_PAY, callback_data='pay.ovpn')])
    inline_kb_list.append([InlineKeyboardButton(text=MAIN_MENU, callback_data='cancel')])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def pay_markup(summ):
    inline_kb_list = [[InlineKeyboardButton(text=PAY_TEXT % (summ), pay=True)],
                    [InlineKeyboardButton(text=MAIN_MENU, callback_data='cancel')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def buy_key_if_empty():
    inline_kb_list = [
        [InlineKeyboardButton(text=NEW_KEY, callback_data='new')], 
        [InlineKeyboardButton(text=MAIN_MENU, callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def help_twice():
    inline_kb_list = [
        [InlineKeyboardButton(text=NEW_KEY, callback_data='help2')], 
        [InlineKeyboardButton(text=MAIN_MENU, callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def help_cancel():
    inline_kb_list = [
        [InlineKeyboardButton(text=MAIN_MENU, callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)