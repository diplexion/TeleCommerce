from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from src.core.locale.LocalesService import get_text
from src.core.database.MongoService import MongoService
from src.feature.keyboards.StaffKeyboard import staff_main_keyboard

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()
mongo = MongoService()

@router.message(Command("staffmenu"))
async def staff_menu_cmd(message: Message) -> None:
    user = await mongo.get_user_from_db(message.from_user.id)

    profile = user.get('PROFILE', {})
    language = profile.get('language', 'ru-RU')

    await message.answer(
        text=get_text("staff.staff_menu", language),
        reply_markup=await staff_main_keyboard(),
        parse_mode="Markdown"
    )
