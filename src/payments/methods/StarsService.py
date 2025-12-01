import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State

from src.database.MongoService import MongoService
from src.language.LocalesService import get_text
from config import Config
"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

logger = logging.getLogger(__name__)
router = Router()
mongo = MongoService()

class  StarsServiceStates(StatesGroup):
    waiting_for_star_amount = State()

@router.callback_query(F.data == "tg_stars")
async def handle_tg_stars(callback_query: CallbackQuery, state: FSMContext):
    user = await mongo.get_user_from_db(callback_query.from_user.id)

    user_data = user.get('PROFILE', {})
    language = user_data.get('language', '')

    await callback_query.message.edit_text(get_text("profile.stars.input_amount", language, exchange_rate=Config.Stars.EXCHANGE_RATE))
    await callback_query.answer()
    await state.set_state(StarsServiceStates.waiting_for_star_amount)

@router.message(StarsServiceStates.waiting_for_star_amount)
async def process_star_amount(message: Message, state: FSMContext):
    user = await mongo.get_user_from_db(message.from_user.id)

    user_data = user.get('PROFILE', {})
    language = user_data.get('language', 'Не установлен')

    try:
        amount = int(message.text)
        if amount <= 0:
            await message.answer(get_text("profile.stars.stars_count_error", language))
            return

        payment_kb = InlineKeyboardBuilder()
        payment_kb.button(text=get_text("profile.stars.pay_stars_button", language), pay=True)

        prices = [LabeledPrice(label='XTR', amount=amount)]

        await message.answer_invoice(
            title="Пополнение баланса",
            description=f"Пополнение баланса с помощью TG Stars: {amount} XTR",
            payload="by stars",
            provider_token='',
            currency="XTR",
            prices=prices,
            reply_markup=payment_kb.as_markup(),
        )
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    try:
        amount = message.successful_payment.total_amount
        user_id = message.from_user.id

        user = await mongo.get_user_from_db(user_id)
        if not user:
            await message.answer("❌ Ошибка: пользователь не найден в базе данных.")
            return

        profile = user.get('PROFILE', {})
        current_stars = profile.get('balance', 0)
        new_balance = current_stars + amount

        await mongo.update_user(user_id, {"PROFILE.balance": new_balance})

        await message.answer(f"✅ Оплата успешна! Ваш новый баланс: {new_balance} ⭐️")
    except Exception as e:
        logger.error(f"Ошибка при обработке успешной оплаты для пользователя {message.from_user.id}: {e}")
        await message.answer("❌ Произошла ошибка при обновлении баланса. Пожалуйста, свяжитесь с поддержкой.")


