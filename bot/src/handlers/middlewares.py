from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import ADMINS


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admin_ids = ADMINS

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
