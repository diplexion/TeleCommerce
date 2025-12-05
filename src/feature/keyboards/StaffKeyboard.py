from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def staff_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Управление товарами", callback_data="manage_products")],
            [InlineKeyboardButton(text="🛒 Управление заказами", callback_data="manage_orders")],
            [InlineKeyboardButton(text="👥 Управление пользователями", callback_data="manage_users")],
            [InlineKeyboardButton(text="📊 Отчеты и аналитика", callback_data="reports_analytics")],
            [InlineKeyboardButton(text="⚙️ Настройки персонала", callback_data="staff_settings")],
        ]
    )
    return keyboard