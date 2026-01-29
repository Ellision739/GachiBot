import json
import os
import asyncio
import logging
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
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    logger.error(f"Ошибка записи в {file_path}: {e}")

            await loop.run_in_executor(self._executor, _write)


# Создаем экземпляр менеджера
db = GachiDataManager()

# Фразы шара
REASON_PHRASES = [
    "Потому что тебя все никак не трахнут",
    "Потому что Билли умер за наши грехи",
    "Потому что кожу содрал",
    "Потому что дверью ошибся",
    "Потому что ты забываешь о том, чему учил наш батя",
    "Потому что танец станцевал",
    "Потому что в фуру к трахобойщикам сел",
    "Потому что пароль oralcumshot поставил",
    "Потому что в качалку не пошёл",
    "Потому что очко не прикрыл",
    "Потому что ты fucken slave!",
    "Потому что ты избранный!",
    "Потому что кожанку одел",
    "Потому что гачи — это судьба",
    "Потому что так сказал Билли",
    "Потому что в подвале не спрашивают",
    "Потому что ремень был снят первым"
]

SHAR_PHRASES = {
    "почему": REASON_PHRASES,

    "зачем": REASON_PHRASES,

    "куда": [
        "В Leather Club, который на два блока ниже",
        "В Deep Dark Fantasies",
        "Прямиком в раздевалку",
        "В душ за 300 баксов",
        "На скамью для жима",
        "В подвал к Dungeon Master'у",
        "В качалку, качать булки",
        "К Ван Даркхолму на кастинг",
        "В самый центр гачи-ремикса",
        "На поиски потерянного масла для тела"
    ],

    "как": [
        "С криком Билли Херрингтона",
        "Смазано и натренировано",
        "В поту и масле",
        "Медленно, но проникающе",
        "Как учили в качалке",
        "По-гачески — глубоко и честно",
        "По приказу Dungeon Master'а",
        "Как последний подход на жим"
    ],

    "где": [
        "В раздевалке спортзала",
        "На скамье для жима",
        "У Билли дома",
        "В качалке, среди мужиков",
        "Под плакатом с Гачимучи-богами",
        "В гачи-подвале",
        "В лесу с лысым мужиком"
    ],

    "кто": [
        "アマヤ",
        "Вадим",
        "Шаман",
        "Витёк",
        "Максим",
        "Костя",
        "Павлова",
        "Ксюша",
        "Лысый",
        "Билли, но только в воображении...",
        "Van Darkholme",
        "Рикардо Милос",
        "Лика Ширикова",
        "Игорь (тот самый)",
        "Босс этой качалки",
        "Крепкий парень с гачи-опытом",
        "Гачи бот"
    ],

    "": [
        "Ответ отрицательный",
        "Нет",
        "Ответ положительный",
        "Да"
    ]
}

JOIN_PHRASES = [
    "Добро пожаловать в качалку, {username}!",
    "Новый факен слэйв присоединился. Закрой очко, {username}!",
    "Встречайте свежую говядину! Welcome, {username}!",
    "Новый раб прибыл в подвал! Привет, {username}!",
    "Собрание началось. С прибытием, {username}!",
    "Готовься к боли и любви. Добро пожаловать, {username}!",
    "Welcome to the club, {username}!",
    "Hey {username}, I think you've got the wrong door. Leather club is two blocks down."
]

LEAVE_PHRASES = [
    "Один из рабов сбежал... прощай, {username}.",
    "{username} ушёл. А очко забыл!",
    "Никто не покидает качалку живым, {username}...",
    "Покойся с миром, {username}.",
    "Система потеряла одного бойца. Ушёл {username}.",
    "Один из нас ушёл в анал истории. До встречи, {username}."
]

CHOICE_PHRASES = [
    "Определённо {}.",
    "Я думаю, что {}.",
    "Лучше {}.",
    "Однозначно {}.",
    "Без сомнений — {}.",
    "Судьба выбирает: {}."
]

SEX_PHRASES = [
    "{sender} мощно шпилит {target} под гачи ремикс.",
    "{sender} сочно трахает в жопу {target}.",
    "{sender} заставляет {target} стонать как never before.",
    "{target} дрожит от каждого движения {sender}.",
    "{sender} и {target} входят в фазу гачи оргазма.",
    "{target} принимает каждый толчок {sender} с благоговением.",
    "{target} забывает слово «нет» рядом с {sender}.",
    "{sender} освобождает внутреннего зверя, глядя на {target}.",
    "{target} покрыт потом, но просит ещё {sender}.",
    "{sender} не даёт передышки {target}, под ритмы ремикса.",
    "{target} не выдерживает мощи {sender} и срывается в крик.",
    "{sender} входит в {target} с достоинством."
]

GACHI_ERRORS = [
    "Дай мне больше прав, чтобы кикнуть этого факен слейва!",
    "Мои кожаные оковы слишком слабы без прав администратора. Сделай меня Boss of this Gym!",
    "Этот слэйв слишком сильно сопротивляется! Дай мне полномочия Dungeon Master'а!",
    "Я не могу отправить его в shower без прав админа. Сделай меня главным!",
    "Fucking coming! Дай мне админку, иначе этот слэйв не покинет мой gym.",
    "Я не могу отправить его в shower без прав админа. Сделай меня главным, и я устрою ему 300 bucks за выход."
]

