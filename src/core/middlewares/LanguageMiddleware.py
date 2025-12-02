from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update

from src.core.database.MongoService import MongoService

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

mongo = MongoService()

class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user_id = None

        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id

        if user_id:
            user_data = await mongo.get_user_from_db(user_id)

            if user_data:
                locale = user_data.get('PROFILE', {}).get('language', 'ru-RU')
            else:

                locale = 'ru-RU'
        else:
            locale = 'ru-RU'

        data['locale'] = locale

        return await handler(event, data)

