from io import BytesIO

from aiogram import types, Dispatcher
from loguru import logger
from tiktok_downloader import InvalidUrl

from tgbot.models.user_tg import UserTG
from tgbot.services.blocking_io_running import run_blocking_io
from tgbot.services.downloading import download_tiktok


async def download(message: types.Message, user: UserTG):
    url = message.text

    try:
        video: BytesIO = await run_blocking_io(download_tiktok, url)
    except InvalidUrl:
        await user.send_message("Неверная ссылка")
        logger.warning(f"{user}: InvalidUrl - \"{url}\"")
        return

    input_file = types.InputFile(video)
    await user.send_video(input_file)


def register_download_handlers(dp: Dispatcher):
    dp.register_message_handler(download, content_types=["text"], is_tiktok=True)
