import vk_api
import random
import os
from dotenv import load_dotenv

load_dotenv()
vk_session = vk_api.VkApi(token=os.getenv("VK_USER_TOKEN"))
vk = vk_session.get_api()


def get_random_quote(owner_id):
    try:
        posts = vk.wall.get(owner_id=owner_id, count=100)['items']
        random.shuffle(posts)
        for post in posts:
            text = post.get("text", "")
            for att in post.get("attachments", []):
                if att['type'] == 'photo':
                    return text, att['photo']['sizes'][-1]['url']
        return "Цитата без фото", None
    except Exception as e:
        return f"Ошибка ВК: {e}", None


def get_video_content(owner_id):
    try:
        videos = vk.video.get(owner_id=owner_id, count=100)['items']
        if not videos:
            return None, None

        v = random.choice(videos)
        video_url = f"https://vk.com/video{v['owner_id']}_{v['id']}"
        title = v.get('title', 'Gachi Video')
        return None, f"{title}\n{video_url}"
    except Exception as e:
        print(f"Ошибка получения видео: {e}")
        return None, None