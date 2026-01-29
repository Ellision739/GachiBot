import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from data_manager import db
import random

router = Router()
ADMIN_ID = int(os.getenv("ADMIN_ID"))


@router.message(F.text.lower().contains("гачи помолчи"))
async def silent_mode(message: Message):
    if message.chat.id in db.silent_chats:
        db.silent_chats.remove(message.chat.id)
        await message.answer("Гачибот снова будет радовать работяг!")
    else:
        db.silent_chats.add(message.chat.id)
        await message.answer("Понял, молчу")


@router.message(F.text.lower().startswith("гачи кик"))
async def kick_handler(message: Message):
    if not message.reply_to_message:
        await message.answer("Укажи пользователя ответом на его сообщение!")
        return

    try:
        await message.chat.ban(message.reply_to_message.from_user.id)
        await message.chat.unban(message.reply_to_message.from_user.id)

        name = db.custom_usernames.get(message.from_user.id, message.from_user.first_name)
        await message.answer(f"{name} удалил факен слэйва из беседы.")

    except TelegramBadRequest as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            await message.answer(random.choice(db.GACHI_ERRORS))
        else:
            await message.answer(f"Ошибка при изгнании: {e}")
    except Exception as e:
        await message.answer(f"Не удалось кикнуть: {e}")

@router.message(F.text.lower().startswith("гачи баг"))
async def bug_report(message: Message, bot):
    bug_text = message.text[8:].strip()
    name = db.custom_usernames.get(message.from_user.id, message.from_user.first_name)
    await bot.send_message(ADMIN_ID, f"Новый баг от {name} (ID: {message.from_user.id}):\n{bug_text}")
    await message.answer("Отправлено главному данжен мастеру!")


@router.message(F.text.lower().startswith("гачи бан"))
async def gachi_ban(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Доступно только главному данжен мастеру")
        return

    target_id = None
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id

    if not target_id:
        await message.answer("Укажи пользователя ответом на его сообщение!")
        return

    old_name = db.custom_usernames.get(target_id)

    if old_name:
        word_to_ban = old_name.lower()
        if word_to_ban not in db.ban_words:
            db.ban_words.append(word_to_ban)
            await db.save_data("ban_words")

    db.custom_usernames[target_id] = "fucking slave"
    await db.save_data("usernames")

    await message.answer("Dungeon Master вынес вердикт: статус этого парня теперь — fucking slave.")