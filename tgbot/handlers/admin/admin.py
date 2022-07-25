from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.models.user import User


async def admin_start(message: Message, user: User):
    await message.reply(f"Hello, admin! {user.id}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
