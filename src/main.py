import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import handlers
from handlers import admin_handlers
from connector import dp, bot
from text.keyboard_text import (
    NEW_KEY,
    PROLONG_KEY,
    RESTART_BOT,
    HELP
)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
    