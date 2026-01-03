import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from dotenv import load_dotenv

import data_manager
from handlers import common, gachi, admin

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    @dp.message.outer_middleware()
    async def global_middleware(handler, event, data):
        # Логика молчанки
        if event.chat.id in data_manager.silent_chats and "гачи помолчи" not in event.text.lower():
            return

        # Логика приветствия
        u_id = event.from_user.id
        if str(u_id) not in data_manager.seen_ids:
            data_manager.seen_ids.add(str(u_id))
            data_manager.save_json(data_manager.SEEN_IDS_FILE, list(data_manager.seen_ids))

            await event.answer('Welcome to the club, buddy! Чтобы узнать мои возможности, напиши "гачи помощь"!')
            if os.path.exists("Gachi privetstvie.jpg"):
                await event.answer_photo(FSInputFile("Gachi privetstvie.jpg"))

        return await handler(event, data)

    dp.include_routers(admin.router, gachi.router, common.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())