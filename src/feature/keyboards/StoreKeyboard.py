from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.locale.LocalesService import get_text

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

async def store_keyboard(language) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text("view_products", language), callback_data="view_products")],
            [InlineKeyboardButton(text=get_text("my_cart", language), callback_data="my_cart")],
            [InlineKeyboardButton(text=get_text("checkout", language), callback_data="checkout")],
        ]
    )
    return keyboard