import logging

from aiogram import Router
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.database.MongoService import MongoService
from src.core.locale.LocalesService import get_text

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

#TODO Recode this ass in future

router = Router()
mongo = MongoService()
logger = logging.getLogger(__name__)

class StartStates(StatesGroup):
    start = State()
    choose_language = State()

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext, locale: str) -> None:
    try:
        user = await mongo.get_user_from_db(message.from_user.id)
        if not user:
            logger.info(f"Пользователь {message.from_user.id} не найден в базе данных, создаем новую запись")
            success = await mongo.add_user(
                ign=message.from_user.first_name,
                user_id=message.from_user.id
            )

            if not success:
                await message.answer("❌ Ошибка при создании профиля. Обратитесь в поддержку.")
                return

            await show_language_selection(message, state)
            return

        profile = user.get('PROFILE', {})
        language = profile.get('language', 'ru-RU')

        welcome_text = get_text("welcome", language, name=message.from_user.first_name)
        await message.answer(welcome_text)

    except Exception as e:
        logger.error(f"Ошибка в функции start для пользователя {message.from_user.id}: {e}")
        await message.answer("❌ При использовании команды /start произошла ошибка. Обратитесь в поддержку.")

async def show_language_selection(message: Message, state: FSMContext) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru-ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en-en")]
        ]
    )

    await message.answer(
        "🌐 Пожалуйста, выберите язык интерфейса:\n\n"
        "Please select your interface language:",
        reply_markup=keyboard
    )
    await state.set_state(StartStates.choose_language)


@router.callback_query(StartStates.choose_language)
async def language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        user_id = callback.from_user.id

        if callback.data == "lang_ru-ru":
            language = "ru-RU"
            response = "✅ Язык установлен на русский"
            notification = "✅ Язык успешно установлен!"
        elif callback.data == "lang_en-en":
            language = "en-US"
            response = "✅ Language set to English"
            notification = "✅ Language successfully set!"
        else:
            await callback.answer("❌ Неизвестный выбор", show_alert=True)
            return

        success = await mongo.update_user(
            user_id,
            {"PROFILE.language": language}
        )

        if success:
            await callback.message.edit_text(response)
            await callback.answer(notification)
        else:
            await callback.answer("❌ Ошибка при сохранении языка", show_alert=True)

        await state.clear()

    except Exception as e:
        logger.error(f"Ошибка при выборе языка для пользователя {callback.from_user.id}: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)

@router.message(Command("language"))
async def language_cmd(message: Message, state: FSMContext) -> None:
    await show_language_selection(message, state)