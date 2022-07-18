import asyncio

from aiogram import Dispatcher, types

from tgbot.models.user_tg import UserTG


async def command_start(message: types.Message, user: UserTG):
    text = f"""
<b>Привет{f', {user.info}' if user.info else ''}!</b>

Отправляй мне ссылку на видео из ТикТока!
    """

    await user.send_message(text)


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])