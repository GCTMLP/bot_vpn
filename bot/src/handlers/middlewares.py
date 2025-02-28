from aiogram.filters import BaseFilter
from aiogram.types import Message, TelegramObject
from config import ADMINS, LOGGING_CONFIG
from aiogram import Bot, Dispatcher, BaseMiddleware
from typing import Callable, Dict, Any, Awaitable


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admin_ids = ADMINS
    
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
