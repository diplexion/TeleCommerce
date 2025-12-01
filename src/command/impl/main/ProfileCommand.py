from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from src.profile.ProfileService import profile

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()

@router.message(Command("profile"))
async def profile_cmd(message: Message) -> None:
    await profile(user_id=message.from_user.id, message=message, request="main")