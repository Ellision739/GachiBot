import random
import datetime


def dynamic_response(trigger):
    if trigger == "когда":
        # Генерируем случайную дату до 90 дней
        future_date = datetime.datetime.now() + datetime.timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        return future_date.strftime("%d.%m.%Y в %H:%M")

    elif trigger == "насколько":
        percent = random.randint(0, 100)
        return f"На {percent}%"

    elif trigger == "сколько":
        amount = random.randint(-10, 1500)
        return str(amount)

    else:
        return None