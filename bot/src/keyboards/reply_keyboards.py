from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text.keyboard_text import(
    NEW_KEY,
    PROLONG_KEY,
    MY_KEYS,
    HELP,
    WRITE_MESSAGE_TO_ALL,
    ADMIN_SHOW_NOT_PROLONG,
    ADMIN_SHOW_USERS,
    ADMIN_SHOW_USERS_KEYS,
    WRITE_MESSAGE_TO_ONE
)

def staff_kb():
    btn_list = [
        [KeyboardButton(text=ADMIN_SHOW_USERS), KeyboardButton(text=ADMIN_SHOW_USERS_KEYS)],
        [KeyboardButton(text=ADMIN_SHOW_NOT_PROLONG), KeyboardButton(text=WRITE_MESSAGE_TO_ALL)],
        [KeyboardButton(text=WRITE_MESSAGE_TO_ONE)]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_list)
    