import logging

from aiogram import Router

from src.core.database.MongoService import MongoService

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

logger = logging.getLogger(__name__)
router = Router()
mongo = MongoService()

#TODO Implement CryptoService functionality