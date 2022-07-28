import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from tgbot.config import load_config
from tgbot.filters import AdminFilter, TikTokFilter
from tgbot.handlers import register_start_handlers, register_download_handlers
from tgbot.handlers.admin import register_admin_handlers
from tgbot.middlewares import ACLMiddleware, LoggingMiddleware
from tgbot.misc import logging
from tgbot.models import db
from tgbot.models.user_tg import UserTG
from tgbot.services.broadcasting import send_to_admins


def register_all_middlewares(dp):
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(LoggingMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(TikTokFilter)


def register_all_handlers(dp):
    register_start_handlers(dp)
    register_download_handlers(dp)
    register_admin_handlers(dp)


async def main():
    logging.setup()

    logger.info("Starting bot")
    config = load_config(".env")

    if config.tg_bot.use_redis:
        storage = RedisStorage2(host=config.redis.host, port=config.redis.port, password=config.redis.password)
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot["config"] = config

    await db.on_startup()
    UserTG.bot = bot

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    await send_to_admins(dp, "Бот запущен")

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await (await bot.get_session()).close()
        await db.on_shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
        raise SystemExit(0)
