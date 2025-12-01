import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.database.MongoService import MongoService
from src.keyboards.ProfileKeyboard import top_up_options_keyboard

from src.payments.methods.CryptoService import router as crypto_router
from src.payments.methods.StarsService import router as stars_router

router = Router()
mongo = MongoService()
logger = logging.getLogger(__name__)

router.include_routers(stars_router,
                       crypto_router)

@router.callback_query(F.data == "top_up_balance")
async def handle_top_up_balance(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Top up balance feature is under development.", reply_markup= await top_up_options_keyboard())