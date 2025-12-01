from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()

@router.message(Command("staffmenu"))
async def staff_menu_cmd(message: Message) -> None:
    pass #TODO: MB IN FUTURE IG