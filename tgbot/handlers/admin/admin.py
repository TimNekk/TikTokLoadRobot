from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.user import User


async def test1(message: Message, state: FSMContext):
    await message.reply("test1")
    await state.set_state("admin")


async def test2(message: Message, state: FSMContext):
    await message.reply("test2")
    if message.text == "stop":
        await message.reply("stop")
        await state.finish()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(test1, commands=["test"])
    dp.register_message_handler(test2, state="admin")
