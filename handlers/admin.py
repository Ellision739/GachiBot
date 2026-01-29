import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from data_manager import db
from config import config
from strings import phrases
from strings.commands import GachiCommands as Cmd

router = Router()


@router.message(F.text.lower().contains(Cmd.MUTE))
async def silent_mode(message: Message):
    if message.chat.id in db.silent_chats:
        db.silent_chats.remove(message.chat.id)
        await db.save_data("silent_chats")
        await message.answer("Гачибот снова будет радовать работяг!")
    else:
        db.silent_chats.add(message.chat.id)
        await db.save_data("silent_chats")
        await message.answer("Понял, молчу")


@router.message(F.text.lower().startswith(Cmd.KICK))
async def kick_handler(message: Message):
    if not message.reply_to_message:
        return await message.answer("Укажи пользователя ответом на его сообщение!")

    try:
        await message.chat.ban(message.reply_to_message.from_user.id)
        await message.chat.unban(message.reply_to_message.from_user.id)

        u_id = message.from_user.id
        name = db.custom_usernames.get(u_id, message.from_user.first_name)
        await message.answer(f"{name} удалил факен слэйва из беседы.")
    except TelegramBadRequest as e:
        await message.answer(random.choice(phrases.GACHI_ERRORS))

@router.message(F.text.lower().startswith(Cmd.BUG))
async def bug_report(message: Message, bot):
    mute_until = db.get_mute_time(message.from_user.id)
    if mute_until:
        phrase = random.choice(phrases.SLAVE_BUG_DENIED).format(
            until=mute_until,
            user_id=message.from_user.id
        )
        await message.reply(phrase)
        return

    raw_bug_text = message.text[len(Cmd.BUG):]
    bug_text = raw_bug_text.lstrip(" ,.!:").strip()

    if not bug_text:
        return await message.answer("Опиши баг, buddy! Например: гачи баг не работает флекс")

    u_id = message.from_user.id
    name = db.custom_usernames.get(u_id, message.from_user.first_name)

    await bot.send_message(config.admin_id, f"Новый баг от {name} (ID: {message.from_user.id}):\n{bug_text}")
    await message.answer("Отправлено главному данжен мастеру!")


@router.message(F.text.lower().startswith(Cmd.BAN))
async def gachi_ban(message: Message):
    if message.from_user.id != config.admin_id:
        return await message.answer("Доступно только главному данжен мастеру")

    if not message.reply_to_message:
        return await message.answer("Укажи пользователя ответом на его сообщение!")

    target_id = message.reply_to_message.from_user.id
    old_name = db.custom_usernames.get(target_id)

    if old_name:
        word = old_name.lower()
        if word not in db.ban_words:
            db.ban_words.append(word)
            await db.save_data("ban_words")

    db.custom_usernames[target_id] = "fucking slave"
    await db.save_data("usernames")
    await message.answer("Dungeon Master вынес вердикт: статус этого парня теперь — fucking slave.")
