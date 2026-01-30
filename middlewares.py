import logging
import os
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, FSInputFile

from data_manager import db
from strings.commands import GachiCommands as Cmd

logger = logging.getLogger(__name__)


class GachiMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        try:
            # Проверка на технические сообщения
            if not isinstance(event, Message) or not event.from_user:
                return await handler(event, data)

            text = event.text or event.caption or ""
            text_lower = text.lower()

            # Молчанка
            if event.chat.id in db.silent_chats:
                if Cmd.MUTE not in text_lower:
                    return

            # Приветствие
            user_id = event.from_user.id

            if user_id not in db.seen_ids:
                db.add_seen_id(user_id)

                try:
                    await event.answer(f'Welcome to the club, buddy! Напиши "{Cmd.HELP}".')

                    photo_path = "Gachi privetstvie.jpg"
                    if os.path.exists(photo_path):
                        await event.answer_photo(FSInputFile(photo_path))

                except Exception as send_error:
                    logger.warning(f"Не удалось поприветствовать {user_id}: {send_error}")

        except Exception as e:
            logger.error(f"Ошибка в GachiMiddleware: {e}", exc_info=True)

        return await handler(event, data)
