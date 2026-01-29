import vk_api
import random
import logging
from typing import Optional, Tuple
from config import config

logger = logging.getLogger(__name__)

class GachiSources:
    VIDEO_GROUP = -150683496
    QUOTE_GROUP = -113661329
    FLEX_GROUP = -165104294


vk_session = vk_api.VkApi(token=config.vk_user_token.get_secret_value())
vk = vk_session.get_api()


def get_random_quote(owner_id: int) -> Tuple[Optional[str], Optional[str]]:
    try:
        response = vk.wall.get(owner_id=owner_id, count=config.vk_post_count)
        posts = response.get('items', [])

        if not posts:
            return "Стену облизали, постов нет", None

        random.shuffle(posts)
        for post in posts:
            text = post.get("text", "")
            attachments = post.get("attachments", [])

            for att in attachments:
                if att['type'] == 'photo':
                    return text, att['photo']['sizes'][-1]['url']

        return "Цитата без фото", None
    except Exception as e:
        logger.error(f"Ошибка ВК: {e}")
        return f"Ошибка ВК: {e}", None


def get_video_content(owner_id: int) -> Tuple[None, Optional[str]]:
    try:
        response = vk.video.get(owner_id=owner_id, count=config.vk_post_count)
        videos = response.get('items', [])

        if not videos:
            return None, None

        v = random.choice(videos)
        video_url = f"https://vk.com/video{v['owner_id']}_{v['id']}"
        title = v.get('title', 'Gachi Video')

        return None, f"{title}\n{video_url}"
    except Exception as e:
        logger.error(f"Ошибка получения видео: {e}")
        return None, None