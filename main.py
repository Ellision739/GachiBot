import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import middlewares
from handlers import common, gachi, admin
from config import config
from data_manager import db

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
        bot = Bot(
            token=config.bot_token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher()

        dp.message.outer_middleware(middlewares.GachiMiddleware())

        dp.include_routers(admin.router, gachi.router, common.router)

        logger.info("Dungeon Master заходит в качалку... (Бот запущен)")

        save_task = asyncio.create_task(db.auto_save_loop(interval=600))

        await bot.delete_webhook(drop_pending_updates=True)

        try:
            await dp.start_polling(bot)
        finally:
            logger.info("Завершение работы. Сохраняем данные...")
            await db.save_all()  # Принудительное сохранение перед смертью
            save_task.cancel()

    except Exception as e:
        logger.critical(f"Бот упал при запуске: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")