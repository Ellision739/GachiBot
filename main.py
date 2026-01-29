import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import middlewares
from handlers import common, gachi, admin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot_log.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    try:
        load_dotenv()
        bot = Bot(token=os.getenv("BOT_TOKEN"))
        dp = Dispatcher()

        dp.message.outer_middleware(middlewares.GachiMiddleware())
        dp.include_routers(admin.router, gachi.router, common.router)

        logger.info("Dungeon Master заходит в качалку... (Бот запущен)")
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Бот упал при запуске: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")