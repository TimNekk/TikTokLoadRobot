from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


music_callback_data = CallbackData("music", "url")


def get_music_callback_data(url: str):
    return music_callback_data.new(url=url)


def music_keyboard(url: str):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text="Скачать звук 🎵", callback_data=get_music_callback_data(url)))

    return keyboard
