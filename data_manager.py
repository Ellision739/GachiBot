import json
import os
import asyncio
import logging
import shutil
import datetime
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class GachiDataManager:
    def __init__(self):
        # Пути к файлам
        self.USERNAMES_FILE = "data/custom_usernames.json"
        self.SEEN_IDS_FILE = "data/seen_ids.json"
        self.BAN_WORDS_FILE = "data/ban_words.json"
        self.SILENT_CHATS_FILE = "data/silent_chats.json"
        self.SLAVE_STATS_FILE = "data/slave_stats.json"
        self.UPDATES_FILE = "data/updates.json"

        # Инструменты асинхронности
        self._executor = ThreadPoolExecutor(max_workers=3)
        self._lock = asyncio.Lock()

        # Загрузка данных
        self.custom_usernames = {int(k): v for k, v in self._load_json(self.USERNAMES_FILE, {}).items()}
        self.seen_ids = set(map(int, self._load_json(self.SEEN_IDS_FILE, [])))
        self.silent_chats = set(self._load_json(self.SILENT_CHATS_FILE, []))
        self.ban_words = self._load_json(self.BAN_WORDS_FILE, ["шаман", "шамов", "данил", "даниил"])
        self.slave_stats = {int(k): v for k, v in self._load_json(self.SLAVE_STATS_FILE, {}).items()}
        self.updates = self._load_json(self.UPDATES_FILE, [])
        self._needs_save = False

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
            "silent_chats": (self.SILENT_CHATS_FILE, list(self.silent_chats)),
            "slave_stats": (self.SLAVE_STATS_FILE, self.slave_stats)
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

    async def auto_save_loop(self, interval=600):
        """Фоновая задача: сохраняет всё на диск раз в 10 минут, если были изменения"""
        logger.info("Цикл автосохранения запущен.")
        while True:
            await asyncio.sleep(interval)
            if self._needs_save:
                await self.save_all()

    async def save_all(self):
        """Принудительное сохранение всех измененных данных на диск"""
        logger.info("Синхронизация данных с диском...")
        # Сохраняем по очереди все важные файлы
        await self.save_data("usernames")
        await self.save_data("seen_ids")
        await self.save_data("slave_stats")
        await self.save_data("silent_chats")
        self._needs_save = False  # Сбрасываем флаг после записи

    def add_seen_id(self, user_id: int):
        """Безопасно добавляет ID и помечает, что нужно сохранение"""
        if user_id not in self.seen_ids:
            self.seen_ids.add(user_id)
            self._needs_save = True

    MUTE_STAGES = [5, 10, 30, 60, 120, 300, 720, 1440]

    def punish_slave(self, user_id: int):
        """Наказывает слэйва: повышает счетчик и ставит время мута."""

        # Получаем текущую статистику или создаем новую
        stats = self.slave_stats.get(user_id, {"count": 0, "mute_until": None})

        # Определяем стадию наказания (не выше последней в списке)
        stage = min(stats["count"], len(self.MUTE_STAGES) - 1)
        minutes = self.MUTE_STAGES[stage]

        # Вычисляем время окончания
        until = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

        # Обновляем статы
        self.slave_stats[user_id] = {
            "count": stats["count"] + 1,
            "mute_until": until.isoformat()
        }

        # Насильно меняем имя на fucking slave
        self.custom_usernames[user_id] = "fucking slave"

        self._needs_save = True

        return minutes  # Возвращаем на сколько минут замутили для уведомления

    def get_mute_time(self, user_id: int) -> str:
        """Проверяет мут и возвращает время в красивом формате или None."""

        stats = self.slave_stats.get(user_id)
        if not stats or not stats.get("mute_until"):
            return None

        until = datetime.datetime.fromisoformat(stats["mute_until"])
        if datetime.datetime.now() < until:
            # Возвращаем сколько осталось или до какого времени
            return until.strftime("%H:%M %d.%m")
        return None

db = GachiDataManager()
