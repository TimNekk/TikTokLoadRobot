from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.user import User


async def test1(message: Message, state: FSMContext):
    await message.reply("test1")
    await state.set_state("admin")


async def test2(message: Message):
    await message.reply("test2")


async def test3(message: Message, state: FSMContext):
    await message.reply("test3")
    await state.finish()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(test1, commands=["test"])
    dp.register_message_handler(test2, state="admin")
    dp.register_message_handler(test3, commands=["stop"], state="admin")
