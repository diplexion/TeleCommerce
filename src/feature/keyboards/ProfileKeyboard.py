from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.locale.LocalesService import get_text

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

async def profile_keyboard(language) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text("profile.top_up_balance.top_up_balance_button", language), callback_data="top_up_balance")],
        ]
    )
    return keyboard

async def back_to_profile_keyboard(language) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text("profile.back_to_profile", language), callback_data="profile")],
        ]
    )
    return keyboard

async def top_up_options_keyboard(language) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text("profile.top_up_balance.top_up_options_stars_button", language), callback_data="tg_stars"),
            InlineKeyboardButton(text=get_text("profile.top_up_balance.top_up_options_crypto_button", language), callback_data="crypto")],
            [InlineKeyboardButton(text=get_text("profile.back_to_profile", language), callback_data="profile")],
        ]
    )
    return keyboard

async def back_to_top_up_options_keyboard(language) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text("profile.top_up_balance.back_to_top_up_balance_button", language), callback_data="top_up_balance")],
        ]
    )
    return keyboard