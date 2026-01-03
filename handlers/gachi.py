import random
import re
import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile

import data_manager
from services import vk_service
from utils import text_utils

router = Router()

@router.message(F.text.lower().contains(" или "))
async def choice_handler(message: Message):
    if "гачи шар" in message.text.lower():
        text = message.text.lower().replace("гачи шар", "").strip()
        options = [opt.strip() for opt in text.split(" или ") if opt.strip()]
        if len(options) >= 2:
            chosen = random.choice(options).replace("?", "")
            await message.reply(random.choice(data_manager.CHOICE_PHRASES).format(chosen))


@router.message(F.text.lower().contains("гачи шар"))
async def gachi_ball(message: Message):
    msg = message.text.lower()

    if re.search(r"да\?$", msg): return await message.reply("пизда!")
    if re.search(r"да$", msg): return await message.reply("пизда")

    triggers = ["почему", "зачем", "как", "где", "кто", "когда", "насколько", "сколько"]
    for tr in triggers:
        if tr in msg:
            if tr in ["когда", "насколько", "сколько"]:
                await message.reply(text_utils.dynamic_response(tr))
            else:
                await message.reply(random.choice(data_manager.SHAR_PHRASES[tr]))
            return

    # Если просто шар
    await message.reply(random.choice(data_manager.SHAR_PHRASES[""]))


@router.message(F.text.lower().startswith("гачи имя"))
async def set_name_handler(message: Message):
    new_name = message.text[8:].strip()
    if not new_name:
        await message.answer("Укажи имя, например: гачи имя Работяга")
        return

    if any(bad in new_name for bad in data_manager.ban_words):
        data_manager.custom_usernames[message.from_user.id] = "fucken slave"
        await message.answer("Oh fuck you, буду звать тебя fucken slave")
    else:
        data_manager.custom_usernames[message.from_user.id] = new_name
        await message.answer(f"Понял, буду звать тебя {new_name}")

    data_manager.save_json(data_manager.USERNAMES_FILE, data_manager.custom_usernames)


@router.message(F.text.lower().contains("гачи цитата"))
async def gachi_quote(message: Message):
    text, photo = vk_service.get_random_quote(-113661329)
    if photo:
        await message.answer_photo(photo, caption=text)
    else:
        await message.answer(text)


@router.message(F.text.lower().startswith("гачи секс"))
async def sex_handler(message: Message):
    if not message.reply_to_message:
        return await message.answer("Чтобы совершить акт, ответь на сообщение партнера!")

    s_id = message.from_user.id
    t_id = message.reply_to_message.from_user.id
    s_name = data_manager.custom_usernames.get(s_id, message.from_user.first_name)
    t_name = data_manager.custom_usernames.get(t_id, message.reply_to_message.from_user.first_name)

    sender = f"<a href='tg://user?id={s_id}'>{s_name}</a>"
    target = f"<a href='tg://user?id={t_id}'>{t_name}</a>"

    phrase = random.choice(data_manager.SEX_PHRASES).format(sender=sender, target=target)
    await message.answer(phrase, parse_mode="HTML")


@router.message(F.text.lower().contains("гачи аудио"))
async def audio_cmd(message: Message):
    music_dir = "music"

    if not os.path.exists(music_dir) or not os.listdir(music_dir):
        return await message.answer("В папке 'music' пусто! Закинь туда свои mp3, Master.")

    await message.answer("Держи, buddy")

    # Случайный файл из папки
    all_songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
    random_song = random.choice(all_songs)
    path = os.path.join(music_dir, random_song)

    await message.answer_audio(
        FSInputFile(path)
    )


@router.message(F.text.lower().contains("гачи видео"))
async def video_cmd(message: Message):
    # Нам нужен только второй аргумент (ссылка)
    _, video_data = vk_service.get_video_content(-150683496)

    if video_data:
        await message.answer(f"Держи, buddy: {video_data}")
    else:
        await message.answer("Босс качалки скрыл все записи.")


@router.message(F.text.lower().contains("гачи флекс"))
async def flex_cmd(message: Message):
    _, flex_data = vk_service.get_video_content(-165104294)

    if flex_data:
        await message.answer(f'Держи, buddy: {flex_data}')
    else:
        await message.answer("Флекс отменяется, раздевалка закрыта.")