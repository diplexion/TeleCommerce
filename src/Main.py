import logging

from aiogram import Router

from src.command.CommandUtility import router as CommandUtility
from src.database.MongoService import MongoService
from src.profile.ProfileService import router as ProfileService
from src.payments.PaymentService import router as PaymentService

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

router = Router()
mongo = MongoService()
logger = logging.getLogger(__name__)

router.include_routers(CommandUtility,
                       ProfileService,
                       PaymentService)

