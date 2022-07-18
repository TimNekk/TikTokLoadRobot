from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


@dataclass
class TikTokFilter(BoundFilter):
    key = 'is_tiktok'
    is_tiktok: bool

    async def check(self, obj):
        if not isinstance(obj, types.Message):
            raise NotImplementedError(f"{type(obj)} is not supported")
        obj: types.Message
        return ("tiktok.com" in obj.text) == self.is_tiktok
