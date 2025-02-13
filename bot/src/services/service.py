import os
from database.repository import SQLAlchemyRepository
from config import NEW_KEY_DIR
from datetime import datetime, timedelta, timezone
from services.shemas import UserShema
from database.models import Keys
from sqlalchemy import select, func
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import shutil
import logging
from logging.config import dictConfig

from config import (
    NEW_KEY_DIR, 
    USED_KEY_DIR, 
    LOGGING_CONFIG
)


ERROR_LOG = logging.getLogger("error")
INFO_LOG = logging.getLogger("info")
dictConfig(LOGGING_CONFIG)


class UserService:
    def __init__(self, user_repo: SQLAlchemyRepository):
        self._user_repo = user_repo()

    def save_start_user(self, user_data: UserShema) -> str:
        try:
            isset = self._user_repo.get_one({'tg_id':user_data.tg_id})
            if isset:
                return 'old'
            self._user_repo.add_one({'tg_id':user_data.tg_id, 
                                    'first_name':user_data.first_name,
                                    'last_name':user_data.last_name, 
                                    'username':user_data.username})
            return 'new'
        except Exception as e:
            ERROR_LOG.error(f'error in save_start_user {str(e)}')

    def get_all_users(self):
        try:
            users = self._user_repo.get_all()
            return [UserShema(tg_id = user.tg_id, 
                                first_name = user.first_name,
                                username=user.username,
                                create_at=user.crated_at) for user in users]
        except Exception as e:
            ERROR_LOG.error(f'error in get_all_users {str(e)}')


class KeyService:
    def __init__(self, 
                user_repo: SQLAlchemyRepository, 
                key_repo: SQLAlchemyRepository):
        self._key_repo = key_repo()
        self._user_repo = user_repo()

    def get_user_id(self, tg_user_id):
        return self._user_repo.get_one({'tg_id': tg_user_id}).id

    def get_user_keys(self, tg_user_id: int) -> list:
        try:
            user_id = self.get_user_id(tg_user_id)
            keys = self._key_repo.get_all({'user_id':user_id})
            return [key.key_name for key in keys]
        except Exception as e:
            ERROR_LOG.error(f'error in get_user_keys {str(e)}')

    def get_user_keys_dates(self, tg_user_id: int) -> list:
        try:
            user_id = self.get_user_id(tg_user_id)
            keys = self._key_repo.get_all({'user_id':user_id})
            return [{'name':key.key_name, 
                    'expire_at':key.expire_at} for key in keys]
        except Exception as e:
            ERROR_LOG.error(f'error in get_user_keys_dates {str(e)}')

    def set_new_key(self, tg_id, period):
        try:
            files = os.listdir(NEW_KEY_DIR)
            nums = [int(f.split('.')[0]) for f in files]
            sorted_nums = sorted(nums)
            name = f'{sorted_nums[0]}.ovpn'
            user_id = self.get_user_id(tg_id)
            added_key = self._key_repo.add_one({'key_name':name, 
                                                'user_id':user_id})
            date_start = added_key.crated_at
            date_start_time = date_start.time()
            expire_date = date_start.date()+relativedelta(months=int(period))
            self._key_repo.update_one(added_key, 
                                    {'expire_at': str(expire_date)+' '+str(date_start_time)})
            shutil.move(NEW_KEY_DIR+name, USED_KEY_DIR+name)
            return str(expire_date)+' '+str(date_start_time), name
        except Exception as e:
            ERROR_LOG.error(f'error in set_new_key {str(e)}')

    def get_expired_keys(self, today=False, soon=False):
        try:
            t_offset = timedelta(hours=3)
            t_zone = timezone(offset=t_offset, name="UTC")
            now = datetime.now(t_zone).date()
            if today:
                keys_expire_sql = select(self._key_repo.model).filter(func.date(self._key_repo.model.expire_at) == now)
            elif soon:
                keys_expire_sql = select(self._key_repo.model).filter((func.date(self._key_repo.model.expire_at)+timedelta(days=1)) == now)
            else:
                keys_expire_sql = select(self._key_repo.model).filter(self._key_repo.model.expire_at < now)
            keys_expire = self._key_repo.native_sql(keys_expire_sql)
            return keys_expire
        except Exception as e:
            ERROR_LOG.error(f'error in get_expired_keys {str(e)}')

    def get_expired_today_keys(self):
        try:
            t_offset = timedelta(hours=3)
            t_zone = timezone(offset=t_offset, name="UTC")
            now = datetime.now(t_zone)
            keys_expire_sql = select(self._key_repo.model).filter(func.date(self._key_repo.model.expire_at) == now.date())
            keys_today_expire = self._key_repo.native_sql(keys_expire_sql)
            return keys_today_expire
        except Exception as e:
            ERROR_LOG.error(f'error in get_expired_today_keys {str(e)}')

    def get_users_keys(self) -> dict:
        try:
            data = {}
            users_keys = self._key_repo.get_all()
            for key in users_keys:
                if data.get(key.user.id):
                    data[key.user.id].append({'first_name':key.user.first_name,
                                                'username':key.user.username,
                                                'key_name': key.key_name,
                                                'expire_at':key.expire_at})
                else:
                    data[key.user.id] = [{'first_name':key.user.first_name,
                                                'username':key.user.username,
                                                'key_name': key.key_name,
                                                'expire_at':key.expire_at}]
            return data
        except Exception as e:
            ERROR_LOG.error(f'error in get_users_keys {str(e)}')

    def prolong_key(self, key_names, prolong_month):
        try:
            for key_name in key_names:
                key = self._key_repo.get_one({'key_name': key_name})
                time = key.expire_at.time()
                new_expire = key.expire_at.date() + relativedelta(months=int(prolong_month))
                self._key_repo.update_one(key, {'expire_at':str(new_expire)+" "+str(time)})
            return new_expire
        except Exception as e:
            ERROR_LOG.error(f'error in prolong_key {str(e)}')
