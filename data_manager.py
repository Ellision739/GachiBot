import json
import os
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

USERNAMES_FILE = "data/custom_usernames.json"
SEEN_IDS_FILE = "data/seen_ids.json"
BAN_WORDS_FILE = "data/ban_words.json"

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=3)


def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка при загрузке {file}: {e}")
            return default
    return default


async def save_json_async(file, data):
    loop = asyncio.get_running_loop()

    def _save():
        try:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except PermissionError:
            logger.error(f"Нет прав на запись файла {file}!")
        except Exception as e:
            logger.error(f"Критическая ошибка при сохранении {file}: {e}")

    await loop.run_in_executor(_executor, _save)

# Глобальные переменные данных
custom_usernames = {int(k): v for k, v in load_json(USERNAMES_FILE, {}).items()}
seen_ids = set(load_json(SEEN_IDS_FILE, []))
silent_chats = set()

ban_words = load_json(BAN_WORDS_FILE, ["шаман", "шамов", "данил", "даниил"])

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