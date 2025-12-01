from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from src.store.StoreService import store

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()

@router.message(Command("store"))
async def store_cmd(message: Message) -> None:
    await store(message, user_id=message.from_user.id)