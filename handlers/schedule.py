import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import bot, ADMINS


async def deadline_hw(bot: Bot):
    await bot.send_message(ADMINS[0], 'Не забудьте о дедлайне дз!')


async def set_scheduler():
    scheduler = AsyncIOScheduler(timezone='Asia/Bishkek')
    scheduler.add_job(
        deadline_hw,
        trigger=CronTrigger(day_of_week='mon,thu', hour=17),
        kwargs={'bot': bot}
    )
    scheduler.start()
