from config import ADMINS, LOGGING_CONFIG
from aiogram import Bot, Dispatcher
import logging
from logging.config import dictConfig
from services.depencies import key_service
from text.message_text import (
    USERS_KEYS_EXPIRE_TEXT,
    USERS_KEYS_EXPIRE,
    USERS_KEYS_EXPIRE_TEXT_SOON
)
from keyboards.inline_keyboards import chose_doing_markup

ERROR_LOG = logging.getLogger("error")
INFO_LOG = logging.getLogger("info")
dictConfig(LOGGING_CONFIG)

async def send_message_to_user_expired_today(bot: Bot):
    try:
        result_data = {}
        not_prolong_keys = key_service().get_expired_keys(today=True)
        for not_prolong_key in not_prolong_keys:
            if result_data.get(not_prolong_key.user.id):
                result_data[not_prolong_key.user.tg_id].append({'key_name': not_prolong_key.key_name,
                                                    'expire_at':not_prolong_key.expire_at})
            else:
                result_data[not_prolong_key.user.tg_id] = [{'key_name': not_prolong_key.key_name,
                                                    'expire_at':not_prolong_key.expire_at}]
        for userid, data in result_data.items():
            result_text = USERS_KEYS_EXPIRE_TEXT
            for one_data in data:
                result_text+=USERS_KEYS_EXPIRE % (one_data['key_name'])
            await bot.send_message(text=result_text, chat_id=userid, reply_markup=chose_doing_markup())
    except Exception as e:
        ERROR_LOG.error(f'Uknown error in send_message_to_user_expired_today {str(e)}')

async def send_message_to_user_expired_soon(bot: Bot):
    try:
        INFO_LOG.info('in soon')
        result_data = {}
        not_prolong_keys = key_service().get_expired_keys(soon=True)
        for not_prolong_key in not_prolong_keys:
            if result_data.get(not_prolong_key.user.id):
                result_data[not_prolong_key.user.tg_id].append({'key_name': not_prolong_key.key_name,
                                                    'expire_at':not_prolong_key.expire_at})
            else:
                result_data[not_prolong_key.user.tg_id] = [{'key_name': not_prolong_key.key_name,
                                                    'expire_at':not_prolong_key.expire_at}]
        for userid, data in result_data.items():
            result_text = USERS_KEYS_EXPIRE_TEXT_SOON
            for one_data in data:
                result_text+=USERS_KEYS_EXPIRE % (one_data['key_name'])
            await bot.send_message(text=result_text, chat_id=userid, reply_markup=chose_doing_markup())
    except Exception as e:
        ERROR_LOG.error(f'Uknown error in send_message_to_user_expired_today {str(e)}')
