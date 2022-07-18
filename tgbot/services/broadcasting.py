import logging

from aiogram import Dispatcher

from tgbot.config import Config


logger = logging.getLogger(__name__)


async def send_to_admins(dp: Dispatcher, text: str):
    config: Config = dp.bot.get('config')
    for admin_id in config.tg_bot.admin_ids:
        try:
            await dp.bot.send_message(admin_id, text)
        except Exception as e:
            logger.exception(e)
