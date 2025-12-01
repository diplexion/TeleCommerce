from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.language.LocalesService import get_text

async def profile_keyboard(language) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text("profile.top_up_balance", language), callback_data="top_up_balance")],
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

async def top_up_options_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Telegram Stars", callback_data="tg_stars")],
            [InlineKeyboardButton(text="Crypto (In development)", callback_data="crypto")]
        ]
    )
    return keyboard