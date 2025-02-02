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
    HELP,
)

def chose_doing_markup():
    inline_kb_list = [
        [InlineKeyboardButton(text=NEW_KEY, callback_data='new')], 
        [InlineKeyboardButton(text=PROLONG_KEY, callback_data='prolong')],
        [InlineKeyboardButton(text=MY_KEYS, callback_data='my_keys')], 
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

def choose_keys_kb(key_names):
    inline_kb_list = [[InlineKeyboardButton(text=name, callback_data=name)] for name in key_names]
    inline_kb_list.append([InlineKeyboardButton(text=PROLONG_ALL, callback_data='all')])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
