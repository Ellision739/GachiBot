from aiogram import Router, F
from aiogram.types import Message
import data_manager
import random

router = Router()

@router.message(F.text.lower() == "гачи помощь")
async def help_cmd(message: Message):
    await message.answer(
        "В круглых скобках указаны обязательные параметры, в квадратных - необязательные. Сами скобки писать не нужно.\n\n"
        
        "Ответы от бота:\n"
        "гачи шар, (вопрос) — ответ на вопрос\n"
        "гачи аудио/видео/флекс — гачиконтент\n"
        "гачи цитата — гачицитата\n\n"
        "гачи имя [текст] — бот будет называть тебя так, как в блоке \"текст\"\n"
        "гачи секс (юзер) — заняться гачи сексом с участником\n"

        "Для администраторов бесед (боту нужна админка для этого):\n"
        "гачи кик (юзер) — кик человека\n"
        "гачи помолчи — бот молчит, пока не будет использована та же команда\n\n"

        "Прочее:\n"
        "Бот имеет скрытые триггеры на различные слова\n"
        "гачи баг (текст бага) — баг-репорт или просто связь с разрабом"
    )

@router.message(F.new_chat_members)
async def welcome(message: Message):
    for user in message.new_chat_members:
        name = user.first_name
        await message.answer(random.choice(data_manager.JOIN_PHRASES).format(username=name))

@router.message(F.left_chat_member)
async def farewell(message: Message):
    name = message.left_chat_member.first_name
    await message.answer(random.choice(data_manager.LEAVE_PHRASES).format(username=name))

@router.message(F.text)
async def text_triggers(message: Message):
    msg_lower = message.text.lower()
    u_id = message.from_user.id
    name = data_manager.custom_usernames.get(u_id, message.from_user.first_name)

    if "сос" in msg_lower: await message.answer(f"Сам соси, {name}")
    elif "ебать ты" in msg_lower: await message.answer(f"Нет, ебать ты, {name}!")
    elif "иди нахуй" in msg_lower: await message.answer(f"Сам иди нахуй, {name}")
    elif "fuck you" in msg_lower: await message.answer(f"Oh, fuck you, {name}!")
    elif any(word in msg_lower for word in ["извин", "прости", "sorry"]): await message.answer(f"Sorry for what, {name}?")
    elif "гачи привет" in msg_lower: await message.answer(f"Приветствую, {name}!")
    elif "фак ю" in msg_lower: await message.answer("Ох, фак ю лезэрмэн!")
    elif "гачи стата" in msg_lower: await message.answer("Ебать ты, ёбаный в жопу ребёнок, обмазанный говном! Ты ебанутый пидорас с силой ацтекского бога мастурбации.")
    elif "хозяин шамана" in msg_lower: await message.answer("У Шамана только один хозяин - это Билли Херрингтон")