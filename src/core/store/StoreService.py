from aiogram import Router

from src.core.locale.LocalesService import get_text
from src.core.database.MongoService import MongoService

from src.feature.keyboards.StoreKeyboard import store_main_keyboard
"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()
mongo = MongoService()

async def store(message, user_id) -> None:
    user = await mongo.get_user_from_db(user_id)

    profile = user.get('PROFILE', {})
    language = profile.get('language', 'ru-RU')

    await message.answer(text=get_text("store.store_main", language),
                         reply_markup=await store_main_keyboard(language))
