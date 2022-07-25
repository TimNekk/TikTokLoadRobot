import re
from io import BytesIO

from aiogram import types, Dispatcher
from loguru import logger
from tiktok_downloader import InvalidUrl

from tgbot.keyboards.inline import music_keyboard, music_callback_data
from tgbot.models.user_tg import UserTG
from tgbot.services.blocking_io_running import run_blocking_io
from tgbot.services.downloading import download_tiktok_video, download_tiktok_music, Music, Video


async def download_video(message: types.Message, user: UserTG):
    await user.send_chat_action("upload_video")
    url = re.findall(r"(https|http)?(://)?(.+)", message.text)[0][-1]
    in_num = re.findall(r"\d{19}", url)
    if in_num:
        url = str(in_num)

    try:
        video: Video = await run_blocking_io(download_tiktok_video, url)
    except InvalidUrl:
        text = f"""
<b>Неверная ссылка</b>

Ссылка должна начинаться с:
  • <code>https://tiktok.com/</code>
  • <code>https://vt.tiktok.com/</code>
"""
        await user.send_message(text)
        logger.warning(f"{user}: InvalidUrl - \"{message.text}\"")
        return

    await user.update(video_download_count=user.video_download_count + 1).apply()

    input_file = types.InputFile(video.data)
    await user.send_video(input_file, caption=f"Скачено в @{(await message.bot.me).username}", reply_markup=music_keyboard(url))


async def download_music(call: types.CallbackQuery, user: UserTG, callback_data: dict):
    await call.message.delete_reply_markup()
    await call.answer()
    url = callback_data.get("url")

    try:
        music: Music = await run_blocking_io(download_tiktok_music, url)
    except InvalidUrl:
        await user.send_message("Произошла ошибка")
        logger.warning(f"{user}: InvalidUrl - \"{url}\"")
        return

    await user.update(audio_download_count=user.audio_download_count + 1).apply()

    input_file = types.InputFile(music.data)
    await user.send_audio(input_file, caption=f"Скачено в @{(await call.bot.me).username}", title=music.title, performer=music.author)


def register_download_handlers(dp: Dispatcher):
    dp.register_message_handler(download_video, content_types=["text"], is_tiktok=True)
    dp.register_callback_query_handler(download_music, music_callback_data.filter())
