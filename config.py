import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    VK_TOKEN = os.getenv("VK_USER_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

    # Настройки путей
    DATA_DIR = "data"
    MUSIC_DIR = "music"

    # Настройки ВК
    VK_POST_COUNT = 100