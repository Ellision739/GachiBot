from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    vk_user_token: SecretStr
    admin_id: int

    # Настройки по умолчанию
    vk_post_count: int = 100

    # Пути
    data_dir: str = "data"
    music_dir: str = "music"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"  # Игнорировать лишние переменные в файле
    }


config = Settings()