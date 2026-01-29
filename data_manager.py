import json
import os
import asyncio
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class GachiDataManager:
    def __init__(self):
        # Пути к файлам
        self.USERNAMES_FILE = "data/custom_usernames.json"
        self.SEEN_IDS_FILE = "data/seen_ids.json"
        self.BAN_WORDS_FILE = "data/ban_words.json"
        self.SILENT_CHATS_FILE = "data/silent_chats.json"

        # Инструменты асинхронности
        self._executor = ThreadPoolExecutor(max_workers=3)
        self._lock = asyncio.Lock()

        # 3. Загрузка данных
        self.custom_usernames = {int(k): v for k, v in self._load_json(self.USERNAMES_FILE, {}).items()}
        self.seen_ids = set(map(str, self._load_json(self.SEEN_IDS_FILE, [])))
        self.silent_chats = set(self._load_json(self.SILENT_CHATS_FILE, []))
        self.ban_words = self._load_json(self.BAN_WORDS_FILE, ["шаман", "шамов", "данил", "даниил"])

    def _load_json(self, file, default):
        """Внутренний метод для загрузки (синхронный, т.к. только при старте)"""
        if os.path.exists(file):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Ошибка загрузки {file}: {e}")
        return default

    async def save_data(self, key: str):
        """
        Универсальный асинхронный метод сохранения.
        key: 'usernames', 'seen_ids', 'ban_words' или 'silent_chats'
        """
        config = {
            "usernames": (self.USERNAMES_FILE, self.custom_usernames),
            "seen_ids": (self.SEEN_IDS_FILE, list(self.seen_ids)),
            "ban_words": (self.BAN_WORDS_FILE, self.ban_words),
            "silent_chats": (self.SILENT_CHATS_FILE, list(self.silent_chats))
        }

        if key not in config:
            return

        file_path, data = config[key]

        async with self._lock:  # Гарантируем, что никто другой не пишет в этот момент
            loop = asyncio.get_running_loop()

            def _write():
                try:
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    if os.path.exists(file_path):
                        shutil.copy2(file_path, f"{file_path}.bak")

                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    logger.error(f"Ошибка записи в {file_path}: {e}")

            await loop.run_in_executor(self._executor, _write)


# Создаем экземпляр менеджера
db = GachiDataManager()
