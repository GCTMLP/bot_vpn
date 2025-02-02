import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from handlers import handlers
from handlers import admin_handlers
from schedule_jobs.jobs import send_message_to_user_expired_today, send_message_to_user_expired_soon
from connector import dp, bot
from text.keyboard_text import (
    NEW_KEY,
    PROLONG_KEY,
    RESTART_BOT,
    HELP
)

def set_scheduled_jobs(scheduler, bot, *args, **kwargs):
    scheduler.add_job(send_message_to_user_expired_today, CronTrigger.from_crontab('0 11 * * *'), args=(bot,))
    scheduler.add_job(send_message_to_user_expired_soon, CronTrigger.from_crontab('0 11 * * *'), args=(bot,))


async def main():
    scheduler = AsyncIOScheduler()
    set_scheduled_jobs(scheduler, bot)
    try:
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")