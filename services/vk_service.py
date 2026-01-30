import vk_api
import random
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Tuple
from config import config

logger = logging.getLogger(__name__)


class VkService:
    # Константы групп
    VIDEO_GROUP = -150683496
    QUOTE_GROUP = -113661329
    FLEX_GROUP = -165104294

    def __init__(self):
        # Инициализация сессии ВК
        self.vk_session = vk_api.VkApi(token=config.vk_user_token.get_secret_value())
        self.vk = self.vk_session.get_api()

        # Пул потоков
        self._executor = ThreadPoolExecutor(max_workers=3)

    def _get_random_quote_sync(self, owner_id: int) -> Tuple[Optional[str], Optional[str]]:
        try:
            # БЛОКИРУЮЩИЙ ЗАПРОС
            response = self.vk.wall.get(owner_id=owner_id, count=config.vk_post_count)
            posts = response.get('items', [])

            if not posts:
                return "Стену облизали, постов нет", None

            random.shuffle(posts)
            for post in posts:
                text = post.get("text", "")
                attachments = post.get("attachments", [])

                for att in attachments:
                    if att['type'] == 'photo':
                        # Берем фото самого лучшего качества
                        return text, att['photo']['sizes'][-1]['url']

            return "Цитата без фото", None
        except Exception as e:
            logger.error(f"Ошибка ВК (посты): {e}")
            return f"Ошибка ВК: {e}", None

    def _get_video_content_sync(self, owner_id: int) -> Tuple[None, Optional[str]]:
        try:
            response = self.vk.video.get(owner_id=owner_id, count=config.vk_post_count)
            videos = response.get('items', [])

            if not videos:
                return None, None

            v = random.choice(videos)
            video_url = f"https://vk.com/video{v['owner_id']}_{v['id']}"
            title = v.get('title', 'Gachi Video')

            return None, f"{title}\n{video_url}"
        except Exception as e:
            logger.error(f"Ошибка ВК (видео): {e}")
            return None, None

    async def get_random_quote(self, owner_id: int) -> Tuple[Optional[str], Optional[str]]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, self._get_random_quote_sync, owner_id)

    async def get_video_content(self, owner_id: int) -> Tuple[None, Optional[str]]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, self._get_video_content_sync, owner_id)


# Создаем один экземпляр сервиса
vk_service = VkService()