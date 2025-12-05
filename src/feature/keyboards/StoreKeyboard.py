import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.core.database.MongoService import MongoService
from src.core.locale.LocalesService import get_text

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

mongo = MongoService()
logger = logging.getLogger(__name__)


async def store_main_keyboard(language) -> InlineKeyboardMarkup:
    try:
        categories = await mongo.get_all_categories()

        if not categories:
            logger.warning("Категории не найдены в базе данных")
            return InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="❌ Нет категорий", callback_data="no_categories")]]
            )

        keyboard_buttons = []
        for category in categories:
            category_name = category.get("NAME", "Unknown")
            callback_data = f"category_{category_name.lower().replace(' ', '_')}"
            button = InlineKeyboardButton(text=category_name, callback_data=callback_data)
            keyboard_buttons.append([button])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        logger.info(f"Клавиатура магазина успешно создана с {len(categories)} категориями")
        return keyboard

    except Exception as e:
        logger.error(f"Ошибка при создании клавиатуры магазина: {e}")
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Ошибка загрузки", callback_data="error")]]
        )
