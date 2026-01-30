from aiogram import Router, F
from aiogram.types import Message
from strings.commands import GachiCommands as Cmd
from strings import phrases
from data_manager import db
import random

router = Router()

@router.message(F.text.lower() == Cmd.HELP)
async def help_cmd(message: Message):
    await message.answer(
        "В круглых скобках указаны обязательные параметры, в квадратных - необязательные. "
        "Сами скобки писать не нужно.\n\n"
        
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


@router.message(F.text.lower() == Cmd.UPDATES)
async def show_updates(message: Message):
    current_updates = db._load_json(db.UPDATES_FILE, [])

    if not current_updates:
        return await message.answer("Пока обновлений не завезли, buddy.")

    text = "<b>GachiBot: Журнал обновлений</b>\n\n"

    # Берем последние 5 обновлений для вывода
    for upd in current_updates[:5]:
        text += (
            f"Версия <b>{upd['id']}</b> ({upd['date']})\n"
            f"<i>{upd['title']}</i>\n"
            f"{upd['description']}\n"
            f"--------------------------------------------------------------\n"
        )

    text += "♂ Stay tuned for more performance ♂"
    await message.answer(text, parse_mode="HTML")


def normalize_text(text: str) -> str:
    """Заменяет английские омографы на русские аналоги и убирает лишние символы"""
    replacements = {
        'a': 'а', 'b': 'в', 'e': 'е', 'k': 'к', 'm': 'м', 'h': 'н',
        'o': 'о', 'p': 'р', 'c': 'с', 't': 'т', 'y': 'у', 'x': 'х'
    }

    text = text.lower()
    for eng, rus in replacements.items():
        text = text.replace(eng, rus)

    return text


@router.message(F.new_chat_members)
async def welcome(message: Message):
    for user in message.new_chat_members:
        name = user.first_name
        await message.answer(random.choice(phrases.JOIN_PHRASES).format(username=name))


@router.message(F.left_chat_member)
async def farewell(message: Message):
    name = message.left_chat_member.first_name
    await message.answer(random.choice(phrases.LEAVE_PHRASES).format(username=name))


@router.message(F.text)
async def text_triggers(message: Message):
    raw_text = message.text.lower()

    msg_normalized = normalize_text(raw_text)

    u_id = message.from_user.id
    name = db.custom_usernames.get(u_id, message.from_user.first_name)

    for key, action in Cmd.ALL_TRIGGERS.items():
        if key in msg_normalized:
            response = action(name) if callable(action) else action
            return await message.reply(response)

    if any(word in msg_normalized for word in Cmd.TRIGGERS_APOLOGY):
        return await message.reply(f"Sorry for what, {name}?")