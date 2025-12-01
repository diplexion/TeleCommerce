import logging

from aiogram import Router

from src.command.impl.main.ProfileCommand import router as ProfileCommandRouter
from src.command.impl.main.StartCommand import router as StartCommandRouter
from src.command.impl.main.InfoCommand import router as InfoCommandRouter
from src.command.impl.main.StoreCommand import router as StoreCommandRouter

from src.command.impl.staff.StaffCommand import router as StaffCommandRouter

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()

try:
    router.include_routers(StartCommandRouter,
                           StoreCommandRouter,
                           ProfileCommandRouter,
                           StaffCommandRouter,
                           InfoCommandRouter)
except Exception as e:
    logging.error(f"Ошибка при подключении роутеров команд: {e}")