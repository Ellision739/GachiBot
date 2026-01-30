class GachiCommands:
    # Префиксы
    PREFIX = "гачи "

    # Админские
    BAN = "гачи бан"
    KICK = "гачи кик"
    MUTE = "гачи помолчи"
    BUG = "гачи баг"

    # Общие
    HELP = "гачи помощь"
    BALL = "гачи шар"
    QUOTE = "гачи цитата"
    SEX = "гачи секс"
    NAME = "гачи имя"
    UPDATES = "гачи обнова"

    # Контент
    VIDEO = "гачи видео"
    FLEX = "гачи флекс"
    AUDIO = "гачи аудио"

    # Триггеры
    TRIGGERS_APOLOGY = ["извин", "прости", "sorry", "сори", "сорян"]
    TRIGGER_HELLO = {
        "гачи привет": lambda name: f"Приветствую, {name}!"
    }
    TRIGGER_MASTER = {
        "хозяин шамана": "У Шамана только один хозяин - это Билли Херрингтон"
    }
    TRIGGERS_ANGRY = {
        "сос": lambda name: f"Сам соси, {name}",
        "ебать ты": lambda name: f"Нет, ебать ты, {name}!",
        "иди нахуй": lambda name: f"Сам иди нахуй, {name}",
        "fuck you": lambda name: f"Oh, fuck you, {name}!",
        "фак ю": "Ох, фак ю лезэрмэн!",
        "гачи стата": "Ебать ты, ёбаный в жопу ребёнок, обмазанный говном! "
                      "Ты ебанутый пидорас с силой ацтекского бога мастурбации."
    }

    ALL_TRIGGERS = {**TRIGGER_HELLO, **TRIGGER_MASTER, **TRIGGERS_ANGRY}