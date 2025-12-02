from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from src.core.locale.LocalesService import get_text
from src.core.database.MongoService import MongoService

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()
mongo = MongoService()

@router.message(Command("info"))
async def info_cmd(message: Message) -> None:
    user = await mongo.get_user_from_db(message.from_user.id)

    profile = user.get('PROFILE', {})
    language = profile.get('language', 'ru-RU')

    await message.answer(text=get_text("info", language), disable_web_page_preview=True)