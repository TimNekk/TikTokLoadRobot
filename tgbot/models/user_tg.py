import typing

from aiogram import types, Bot
from aiogram.types import base
from aiogram.utils import exceptions
from loguru import logger

from tgbot.models.user import User


class UserTG(User):
    bot: Bot

    @property
    def info(self) -> typing.Optional[str]:
        if self.first_name:
            return self.first_name
        elif self.username:
            return self.username
        elif self.last_name:
            return self.last_name

    async def _execute_telegram_action(self, action: typing.Callable, *args, **kwargs):
        try:
            return await action(self.id, *args, **kwargs)
        except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated) as e:
            logger.debug(f"{self}: {e.match}")
            await self.update(is_banned=True).apply()
        except exceptions.TelegramAPIError as e:
            logger.exception(f"{self}: {e}")

    async def send_message(self,
                           text: base.String,
                           parse_mode: typing.Optional[base.String] = None,
                           entities: typing.Optional[typing.List[types.MessageEntity]] = None,
                           disable_web_page_preview: typing.Optional[base.Boolean] = None,
                           disable_notification: typing.Optional[base.Boolean] = None,
                           protect_content: typing.Optional[base.Boolean] = None,
                           reply_to_message_id: typing.Optional[base.Integer] = None,
                           allow_sending_without_reply: typing.Optional[base.Boolean] = None,
                           reply_markup: typing.Union[types.InlineKeyboardMarkup,
                                                      types.ReplyKeyboardMarkup,
                                                      types.ReplyKeyboardRemove,
                                                      types.ForceReply, None] = None,
                           ) -> types.Message:
        return await self._execute_telegram_action(self.bot.send_message,
                                                   text,
                                                   parse_mode,
                                                   entities,
                                                   disable_web_page_preview,
                                                   disable_notification,
                                                   protect_content,
                                                   reply_to_message_id,
                                                   allow_sending_without_reply,
                                                   reply_markup)

    async def send_video(self, video: typing.Union[base.InputFile, base.String],
                         duration: typing.Optional[base.Integer] = None,
                         width: typing.Optional[base.Integer] = None,
                         height: typing.Optional[base.Integer] = None,
                         thumb: typing.Union[base.InputFile, base.String, None] = None,
                         caption: typing.Optional[base.String] = None,
                         parse_mode: typing.Optional[base.String] = None,
                         caption_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
                         supports_streaming: typing.Optional[base.Boolean] = None,
                         disable_notification: typing.Optional[base.Boolean] = None,
                         protect_content: typing.Optional[base.Boolean] = None,
                         reply_to_message_id: typing.Optional[base.Integer] = None,
                         allow_sending_without_reply: typing.Optional[base.Boolean] = None,
                         reply_markup: typing.Union[types.InlineKeyboardMarkup,
                                                    types.ReplyKeyboardMarkup,
                                                    types.ReplyKeyboardRemove,
                                                    types.ForceReply, None] = None,
                         ) -> types.Message:
        return await self._execute_telegram_action(self.bot.send_video,
                                                   video,
                                                   duration,
                                                   width,
                                                   height,
                                                   thumb,
                                                   caption,
                                                   parse_mode,
                                                   caption_entities,
                                                   supports_streaming,
                                                   disable_notification,
                                                   protect_content,
                                                   reply_to_message_id,
                                                   allow_sending_without_reply,
                                                   reply_markup)
