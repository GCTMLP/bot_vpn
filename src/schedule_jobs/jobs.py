from config import ADMINS
from aiogram import Bot, Dispatcher
from services.depencies import key_service
from text.message_text import (
    USERS_KEYS_EXPIRE_TEXT,
    USERS_KEYS_EXPIRE,
    USERS_KEYS_EXPIRE_TEXT_SOON,
    USERS_KEYS_EXPIRE_SOON
)
from keyboards.inline_keyboards import chose_doing_markup


async def send_message_to_user_expired_today(bot: Bot):
    result_data = {}
    not_prolong_keys = key_service().get_expired_keys(today=True)
    for not_prolong_key in not_prolong_keys:
        if result_data.get(not_prolong_key.user.id):
            result_data[not_prolong_key.user.id].append({'key_name': not_prolong_key.key_name,
                                                'expire_at':not_prolong_key.expire_at})
        else:
            result_data[not_prolong_key.user.id] = [{'key_name': not_prolong_key.key_name,
                                                'expire_at':not_prolong_key.expire_at}]
    for userid, data in result_data.values():
        result_text = USERS_KEYS_EXPIRE_TEXT
        for one_data in data:
            result_text+=USERS_KEYS_EXPIRE % (one_data['key_name'])
        await bot.send_message(text=result_text, chat_id=userid, reply_markup=chose_doing_markup())


async def send_message_to_user_expired_soon(bot: Bot):
    result_data = {}
    not_prolong_keys = key_service().get_expired_keys(soon=True)
    for not_prolong_key in not_prolong_keys:
        if result_data.get(not_prolong_key.user.id):
            result_data[not_prolong_key.user.id].append({'key_name': not_prolong_key.key_name,
                                                'expire_at':not_prolong_key.expire_at})
        else:
            result_data[not_prolong_key.user.id] = [{'key_name': not_prolong_key.key_name,
                                                'expire_at':not_prolong_key.expire_at}]
    for userid, data in result_data.values():
        result_text = USERS_KEYS_EXPIRE_TEXT_SOON
        for one_data in data:
            result_text+=USERS_KEYS_EXPIRE_SOON % (one_data['key_name'], one_data['key_name'].date())
        await bot.send_message(text=result_text, chat_id=userid)

