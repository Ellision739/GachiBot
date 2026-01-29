import logging
import os
import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message, FSInputFile
import data_manager

logger = logging.getLogger(__name__)


class GachiMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        try:
            # Проверка на None для безопасности
            if not event or not event.from_user:
                return await handler(event, data)

            text = event.text or event.caption or ""
            text_lower = text.lower()

            # Молчанка
            if event.chat.id in data_manager.silent_chats:
                if "гачи помолчи" not in text_lower:
                    return

            # Приветствие
            user_id = str(event.from_user.id)
            if user_id not in data_manager.seen_ids:
                data_manager.seen_ids.add(user_id)

                # Сохраняем в фоне
                asyncio.create_task(
                    data_manager.save_json_async(data_manager.SEEN_IDS_FILE, list(data_manager.seen_ids)))

                try:
                    await event.answer('Welcome to the club, buddy! Напиши "гачи помощь".')

                    photo_path = "Gachi privetstvie.jpg"
                    if os.path.exists(photo_path):
                        await event.answer_photo(FSInputFile(photo_path))
                except Exception as send_error:
                    logger.warning(f"Не удалось отправить приветствие пользователю {user_id}: {send_error}")

        except Exception as e:
            logger.error(f"Ошибка в GachiMiddleware: {e}", exc_info=True)

        return await handler(event, data)