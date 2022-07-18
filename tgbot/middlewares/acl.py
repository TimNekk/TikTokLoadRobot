from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.models.user import User


class ACLMiddleware(BaseMiddleware):
    @staticmethod
    async def set_data(telegram_user: types.User, data: dict):
        user = await User.get(telegram_user.id)
        if user is None:
            user = User(
                id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name
            )
            await user.create()

        data["user"] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.set_data(message.from_user, data)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        await self.set_data(callback_query.from_user, data)
