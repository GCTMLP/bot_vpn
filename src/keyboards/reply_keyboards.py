from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text.keyboard_text import(
    NEW_KEY,
    PROLONG_KEY,
    MY_KEYS,
    HELP,
    ADMIN_PROLONG_KEY,
    ADMIN_SHOW_NOT_PROLONG,
    ADMIN_SHOW_USERS,
    ADMIN_SHOW_USERS_KEYS
)

def staff_kb():
    btn_list = [
        [KeyboardButton(text=ADMIN_SHOW_USERS), KeyboardButton(text=ADMIN_SHOW_USERS_KEYS)],
        [KeyboardButton(text=ADMIN_SHOW_NOT_PROLONG), KeyboardButton(text=ADMIN_PROLONG_KEY)]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_list)
    