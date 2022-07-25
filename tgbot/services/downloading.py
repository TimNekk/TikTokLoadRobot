from dataclasses import dataclass
from io import BytesIO

from requests.exceptions import MissingSchema
from tiktok_downloader import info_post, InvalidUrl


@dataclass
class Video:
    data: BytesIO


@dataclass
class Music:
    data: BytesIO
    title: str
    author: str


def _get_info(url: str):
    try:
        return info_post(url)
    except MissingSchema:
        return info_post(f"https://{url}")
    except KeyError:
        raise InvalidUrl()


def download_tiktok_video(url: str) -> Video:
    info = _get_info(url)
    data = info.download()
    data.seek(0)
    return Video(data)


def download_tiktok_music(url: str) -> Music:
    info = _get_info(url)
    data = info.download_music()
    data.seek(0)
    return Music(data, info.music_title, info.music_author)
