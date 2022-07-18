from io import BytesIO

from tiktok_downloader import info_post


def download_tiktok(url: str) -> BytesIO:
    info = info_post(url)
    video = info.download()
    video.seek(0)
    return video
