from services.shemas import UserShema
import os
from database.repository import SQLAlchemyRepository
from config import NEW_KEY_DIR
from datetime import datetime, timedelta
from services.shemas import UserShema
from database.models import Keys
from sqlalchemy import select


class UserService:
    def __init__(self, user_repo: SQLAlchemyRepository):
        self._user_repo = user_repo()

    def save_start_user(self, user_data: UserShema) -> str:
        try:
            isset = self._user_repo.get_one({'tg_id':user_data.tg_id})
            if isset:
                return 'old'
            self._user_repo.add_one(user_data.model_dump())
            return 'new'
        except Exception as e:
            print(f'error in save_start_user {str(e)}')
            return False

    def get_all_users(self):
        users = self._user_repo.get_all()
        return [UserShema(tg_id = user.tg_id, 
                            first_name = user.first_name,
                            username=user.username,
                            create_at=user.crated_at) for user in users]


class KeyService:
    def __init__(self, user_repo: SQLAlchemyRepository, key_repo: SQLAlchemyRepository):
        self._key_repo = key_repo()
        self._user_repo = user_repo()

    def get_user_id(self, tg_user_id):
        return self._user_repo.get_one({'tg_id': tg_user_id}).id

    def get_user_keys(self, tg_user_id: int) -> list:
        user_id = self.get_user_id(tg_user_id)
        keys = self._key_repo.get_all({'user_id':user_id})
        return [key.key_name for key in keys]

    def get_user_keys_dates(self, tg_user_id: int):
        user_id = self.get_user_id(tg_user_id)
        keys = self._key_repo.get_all({'user_id':user_id})
        return [{'name':key.key_name, 'expire_at':key.expire_at} for key in keys]

    def set_new_key(self, tg_id, period):
        files = os.listdir(NEW_KEY_DIR)
        nums = [int(f.split('.')[0]) for f in files]
        sorted_nums = sorted(nums)
        name = f'{sorted_nums[0]}.ovpn'
        user_id = self.get_user_id(tg_user_id)
        added_key = self._key_repo.add_one({'key_name':name, 'user_id':user_id})
        date_start = added_key.create_at
        expire_date = date_start+timedelta(month=period)
        self._key_repo.update(added_key, {'expire_at': expire_date})

    def update_expire_date(self, key_name, period):
        key = self._key_repo.get_one({'key_name': key_name})
        date_start = key.expire_at
        expire_date = date_start+timedelta(month=period)
        self._key_repo.update(key, {'expire_at': expire_date})

    def get_expired_keys(self):
        now = datetime.now()
        keys_expire_sql = select(self._key_repo.model).filter(self._key_repo.model.expire_at < str(now))
        keys_expire = self._key_repo.native_sql(keys_expire_sql)
        return keys_expire

    def get_users_keys(self):
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
