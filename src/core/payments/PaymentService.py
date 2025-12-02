import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.core.database.MongoService import MongoService
from src.feature.keyboards.ProfileKeyboard import top_up_options_keyboard
from src.core.locale.LocalesService import get_text

from src.core.payments.methods.CryptoService import router as crypto_router
from src.core.payments.methods.StarsService import router as stars_router

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()
mongo = MongoService()
logger = logging.getLogger(__name__)

router.include_routers(stars_router,
                       crypto_router)
@router.callback_query(F.data == "back_to_top_up_options")
async def handle_back_to_top_up_options(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()

    user = await mongo.get_user_from_db(callback_query.from_user.id)

    user_data = user.get('PROFILE', {})
    language = user_data.get('language', '')

    await callback_query.message.edit_text(get_text("profile.top_up_balance.top_up_balance_title", language),
                                           reply_markup= await top_up_options_keyboard(language))

@router.callback_query(F.data == "top_up_balance")
async def handle_top_up_balance(callback_query: CallbackQuery):
    user = await mongo.get_user_from_db(callback_query.from_user.id)

    user_data = user.get('PROFILE', {})
    language = user_data.get('language', '')

    await callback_query.message.edit_text(get_text("profile.top_up_balance.top_up_balance_title", language),
                                           reply_markup= await top_up_options_keyboard(language))