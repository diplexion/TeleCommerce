import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery

from src.database.MongoService import MongoService
from src.language.LocalesService import get_text
from src.keyboards.ProfileKeyboard import profile_keyboard

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()
logger = logging.getLogger(__name__)
mongo = MongoService()

@router.callback_query(F.data == "profile")
async def profile_callback(query: CallbackQuery) -> None:
    await profile(query.message, query.from_user.id)
    await query.answer()

async def profile(message, user_id) -> None:
    try:
        user = await mongo.get_user_from_db(user_id)
        if not user:
            await message.answer("❌ Профиль не найден. Пожалуйста, используйте /start для создания профиля.")
            return

        user_data = user.get('PROFILE', {})
        language = user_data.get('language', 'Не установлен')
        balance = user_data.get('balance', 0)
        reg_date = user.get('FIRST_JOIN', '')

        profile_text = get_text("profile.profile_main", language, id=user_id,
                                language=language,
                                balance=balance,
                                registration_date=reg_date)

        await message.answer(profile_text, parse_mode=ParseMode.MARKDOWN, reply_markup= await profile_keyboard(language))

    except Exception as e:
        logger.error(f"Ошибка в функции profile для пользователя {message.from_user.id}: {e}")
        await message.answer("❌ При использовании команды /profile произошла ошибка. Обратитесь в поддержку.")