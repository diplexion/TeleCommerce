import asyncio
import os
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from config import Config
from src.Main import router as main_router
from src.database.MongoService import MongoService
from src.middlewares.LanguageMiddleware import LanguageMiddleware

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

load_dotenv('./.env')

logger = logging.getLogger(__name__)
mongo = MongoService()

language_middleware = LanguageMiddleware()

bot_token = os.getenv('BOT_TOKEN')
if not bot_token:
    raise ValueError('Токен не найден в .env файле!')

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(main_router)

async def setup_middlewares():
    dp.update.outer_middleware(language_middleware)

async def on_startup():
    await setup_middlewares()
    logger.info("Бот запущен и готов к работе")

    mongo.clear_all_cache()
    logger.info("Кэш очищен при запуске")


async def on_shutdown():
    logger.info("Бот остановлен")


async def main() -> None:
    logger.info("Запуск бота..")

    bot = Bot(token=bot_token, timeout=60, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

    try:
        client = AsyncIOMotorClient(Config.Database.MONGO_URI, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        logger.info("Подключение к MongoDB успешно установлено.")

        await mongo.create_db()
        logger.info("Проверка базы данных завершена")

    except ConnectionFailure as e:
        logger.error(f"Ошибка подключения к MongoDB: {e}")
        return
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        return

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook очищен, начинаем polling...")

        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()
        mongo.client.close()
        logger.info("Соединения закрыты")


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем (Ctrl+C)")
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске: {e}")