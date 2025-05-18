import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from handlers import admin_handlers
from handlers import handlers
from schedule_jobs.jobs import (
    send_message_to_user_expired_today,
    send_message_to_user_expired_soon
)

from connector import dp, bot


every_day_cron = '0 9 * * *'
every_minute_cron = '* * * * * '


def set_scheduled_jobs(scheduler, bot, *args, **kwargs):
    scheduler.add_job(
        send_message_to_user_expired_today,
        CronTrigger.from_crontab(every_day_cron),
        args=(bot,))
    scheduler.add_job(
        send_message_to_user_expired_soon,
        CronTrigger.from_crontab(every_day_cron),
        args=(bot,))


async def main():
    scheduler = AsyncIOScheduler()
    set_scheduled_jobs(scheduler, bot)
    try:
        handlers.message_scheduler.start()
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")