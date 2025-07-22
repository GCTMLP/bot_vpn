from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import F
from aiogram.filters import Command
import logging
from logging.config import dictConfig

from services.shemas import UserShema
from connector import dp, bot
from handlers.middlewares import IsAdmin
from text.keyboard_text import (
    WRITE_MESSAGE_TO_ALL,
    ADMIN_SHOW_NOT_PROLONG,
    ADMIN_SHOW_USERS,
    ADMIN_SHOW_USERS_KEYS,
    WRITE_MESSAGE_TO_ONE
)
from text.message_text import (
    USERS_DATA,
    CHOOSE_ADMIN,
    EXPIRE_KEYS,
    USERS_KEYS_USER,
    USERS_KEYS_KEYS
)
from keyboards.reply_keyboards import (
    staff_kb
)
from keyboards.inline_keyboards import (
    chose_doing_markup
)
from services.depencies import user_service, key_service
from config import LOGGING_CONFIG

ERROR_LOG = logging.getLogger("error")
INFO_LOG = logging.getLogger("info")

dictConfig(LOGGING_CONFIG)


@dp.message(IsAdmin(), Command('admin'))
async def cmd_admin(message: Message):
    await message.answer(CHOOSE_ADMIN, reply_markup=staff_kb())


@dp.message(IsAdmin(), F.text == ADMIN_SHOW_USERS)
async def show_users(message: Message):
    try:
        all_users = user_service().get_all_users()
        result = ''
        for user in all_users:
            result += USERS_DATA % (user.first_name,
                                    user.username,
                                    user.create_at)
        await message.answer(result, reply_markup=staff_kb())
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in show_users: {str(e)}')


@dp.message(IsAdmin(), F.text == ADMIN_SHOW_NOT_PROLONG)
async def show_not_prolong(message: Message):
    try:
        not_prolong_keys = key_service().get_expired_keys()
        result = ''
        for key in not_prolong_keys:
            result += EXPIRE_KEYS % (
                key.user.first_name,
                key.user.username,
                key.key_name,
                key.expire_at)
        await message.answer(
            result,
            reply_markup=staff_kb())
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in show_not_prolong: {str(e)}')


@dp.message(IsAdmin(), F.text == ADMIN_SHOW_USERS_KEYS)
async def show_users_keys(message: Message):
    try:
        users_keys = key_service().get_users_keys()
        result = ''
        for user_keys in users_keys.values():
            result += USERS_KEYS_USER % (
                user_keys[0]['first_name'],
                user_keys[0]['username'])
            for keys in user_keys:
                result += USERS_KEYS_KEYS % (
                    keys['key_name'],
                    keys['expire_at'])
        await message.answer(
            result,
            reply_markup=staff_kb())
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in show_users_keys: {str(e)}')


@dp.message(IsAdmin(), F.text == WRITE_MESSAGE_TO_ALL)
async def write_to_all(message: Message):
    try:
        await message.answer(
            "Напишите сообщение, начинающееся с 'msg'",
            reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in write_to_all: {str(e)}')


@dp.message(IsAdmin(), F.text == WRITE_MESSAGE_TO_ONE)
async def write_to_one(message: Message):
    try:
        await message.answer(
            """Напишите сообщение, начинающееся с 'id' затем '&id человека',
             затем &сообщение""",
            reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in write_to_one: {str(e)}')


@dp.message(IsAdmin(), F.text.contains('msg'))
async def write_to_all_msg(message: Message):
    try:
        users: UserShema = user_service.get_all_users()
        for user in users:
            message_to_users = str(message.text).split('msg ')[1]
            bot.send_message(text=str(message_to_users), chat_id=user.tg_id)
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in write_to_all_msg: {str(e)}')


@dp.message(IsAdmin(), F.text.contains('id'))
async def write_to_one_msg(message: Message):
    try:
        _, user_id, message = message.text.split('&')
        await bot.send_message(
            chat_id=user_id,
            text=f"Ответ поддержки: \n{message}",
            reply_markup=chose_doing_markup())
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in write_to_one_msg: {str(e)}')
