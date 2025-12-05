import functools
import logging
import time
from datetime import datetime, timedelta

import motor.motor_asyncio

from config import Config

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

#TODO Recode MongoService cuz it poor now (make more localized error handling)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def async_log_execution_time(func):

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper

class MongoService:
    def __init__(
        self,
        uri: str = Config.Database.MONGO_URI,
        db_name: str = Config.Database.DB_NAME,
        users_collection: str = Config.Database.USER_COLLECTION_NAME,
        category_collection: str = Config.Database.CATEGORY_COLLECTION_NAME
    ):
        self.cache = {}
        self.uri = uri or "mongodb://localhost:27017"
        self.db_name = db_name or "TeleCommerce"
        self.users_collection_name = users_collection or "users"
        self.create_category_collection = category_collection or "categories"

        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            self.uri,
            maxPoolSize=50,
            minPoolSize=10,
            serverSelectionTimeoutMS=5000
        )
        self.db = self.client[self.db_name]

    # ------------------- DECORATORS ------------------- #
    def cached(self, ttl_seconds=300):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                if cache_key in self.cache:
                    entry = self.cache[cache_key]
                    if datetime.now() < entry["expires"]:
                        logger.debug(f"Cache hit for {func.__name__}")
                        return entry["data"]
                logger.debug(f"Cache miss for {func.__name__}")
                result = await func(*args, **kwargs)
                self.cache[cache_key] = {
                    "data": result,
                    "expires": datetime.now() + timedelta(seconds=ttl_seconds)
                }
                return result
            return wrapper
        return decorator

    def clear_cache_by_prefix(self, prefix):
        keys_to_delete = [k for k in self.cache.keys() if k.startswith(prefix)]
        for key in keys_to_delete:
            del self.cache[key]
        logger.debug(f"Кэш очищен для префикса {prefix}, удалено {len(keys_to_delete)} записей")

    def clear_all_cache(self):
        self.cache.clear()
        logger.info("Кэш полностью очищен")

    # ------------------- MAIN FUNCTIONS ------------------- #
    async def create_db(self):
        try:
            search_db = await self.client.list_database_names()
            if self.db_name in search_db:
                logger.info(f"База данных {self.db_name} уже существует")
                return True
            users_collection = self.db[self.users_collection_name]
            await users_collection.create_index("USER_ID", unique=True)

            logger.info(f"База данных {self.db_name} успешно создана")
            return False
        except Exception as e:
                logger.error(f"Ошибка при создании базы данных: {e}")
                return False

    @property
    def users_collection(self):
        return self.db[self.users_collection_name]

    @property
    def category_collection(self):
        return self.db[self.create_category_collection]

    # ------------------- USERS ------------------- #
    @async_log_execution_time
    async def add_user(self, ign, user_id):
        try:
            existing_user = await self.users_collection.find_one({"USER_ID": user_id})
            if existing_user:
                logger.info(f"Пользователь с USER_ID {user_id} уже существует")
                return True
            user_data = {
                "IGN": ign,
                "USER_ID": user_id,
                "FIRST_JOIN": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "STAFF": False,
                "PROFILE": {
                    "language": "ru-RU",
                    "purchases": 0,
                    "balance": 0
                }
            }
            result = await self.users_collection.insert_one(user_data)
            logger.info(f"Пользователь с USER_ID {user_id} успешно добавлен")
            return bool(result.inserted_id)
        except Exception as e:
            logger.error(f"Ошибка при добавлении пользователя: {e}")
            return False

    @async_log_execution_time
    async def del_user(self, user_id):
        try:
            result = await self.users_collection.delete_one({"USER_ID": user_id})
            success = result.deleted_count > 0
            if success:
                logger.info(f"Пользователь с USER_ID {user_id} успешно удален")
            else:
                logger.warning(f"Пользователь с USER_ID {user_id} не найден")
            return success
        except Exception as e:
            logger.error(f"Ошибка при удалении пользователя: {e}")
            return False


    @async_log_execution_time
    async def update_user(self, user_id, update_fields: dict) -> bool:
        try:
            result = await self.users_collection.update_one(
                {"USER_ID": user_id},
                {"$set": update_fields}
            )
            if result.matched_count == 0:
                logger.warning(f"Пользователь с USER_ID {user_id} не найден для обновления")
                return False
            if result.modified_count > 0:
                logger.info(f"Пользователь с USER_ID {user_id} успешно обновлен: {update_fields}")
            else:
                logger.info(f"Данные пользователя с USER_ID {user_id} уже актуальны: {update_fields}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при обновлении пользователя: {e}")
            return False

    @async_log_execution_time
    async def get_all_users(self, request=None):
        try:
            if request is None:
                users = []
                async for user in self.users_collection.find({"IGN": {"$exists": True}}):
                    users.append(user)
                return users
            elif request == 'Find':
                users_count = await self.users_collection.count_documents({})
                staff_users_count = await self.users_collection.count_documents({"STAFF": True})
                return users_count, staff_users_count
            else:
                logger.warning(f"Неизвестный запрос: {request}")
                return []
        except Exception as e:
            logger.error(f"Ошибка при получении пользователей: {e}")
            return []

    @async_log_execution_time
    async def get_user_from_db(self, user_id: int):
        try:
            user_data = await self.users_collection.find_one({"USER_ID": user_id})
            return user_data
        except Exception as e:
            logger.error(f"Ошибка при получении пользователя: {e}")
            return None

    # --------------- STAFF --------------- #
    @async_log_execution_time
    async def add_staff(self, user_id):
        try:
            user = await self.users_collection.find_one({"USER_ID": user_id})
            if not user:
                logger.warning(f"Пользователь с USER_ID {user_id} не найден")
                return False
            result = await self.users_collection.update_one(
                {"USER_ID": user_id},
                {"$set": {"STAFF": True}}
            )
            success = result.modified_count > 0
            if success:
                logger.info(f"Пользователь с USER_ID {user_id} добавлен в штат")
            else:
                logger.warning(f"Не удалось добавить пользователя с USER_ID {user_id} в штат")
            return success
        except Exception as e:
            logger.error(f"Ошибка при добавлении пользователя в штат: {e}")
            return False

    @async_log_execution_time
    async def remove_staff(self, user_id):
        try:
            user = await self.users_collection.find_one({"USER_ID": user_id})
            if not user:
                logger.warning(f"Пользователь с USER_ID {user_id} не найден")
                return False
            result = await self.users_collection.update_one(
                {"USER_ID": user_id},
                {"$set": {"STAFF": False}}
            )
            success = result.modified_count > 0
            if success:
                logger.info(f"Пользователь с USER_ID {user_id} удален из штата")
            else:
                logger.warning(f"Не удалось удалить пользователя с USER_ID {user_id} из штата")
            return success
        except Exception as e:
            logger.error(f"Ошибка при удалении пользователя из штата: {e}")
            return False

    @async_log_execution_time
    async def check_staff(self, user_id):
        try:
            user_data = await self.get_user_from_db(user_id)
            if not user_data:
                logger.warning(f"Пользователь с USER_ID {user_id} не найден")
                return False
            is_staff = bool(user_data.get('STAFF', False))
            logger.info(f"Проверка статуса staff для пользователя {user_id}: {is_staff}")
            return is_staff
        except Exception as e:
            logger.error(f"Ошибка при проверке статуса сотрудника: {e}")
            return False

    @async_log_execution_time
    async def get_staff_users(self, request=None):
        if request is None:
            try:
                staff_users = []
                async for user in self.users_collection.find(
                    {"STAFF": True},
                    {"USER_ID": 1, "username": 1, "_id": 0}
                ):
                    staff_users.append({
                        "user_id": user["USER_ID"],
                        "username": user.get("username", "No username")
                    })
                if not staff_users:
                    logger.warning("Не найдено пользователей со статусом STAFF")
                    return []
                logger.info(f"Найдено {len(staff_users)} пользователей со статусом STAFF")
                return staff_users
            except Exception as e:
                logger.error(f"Ошибка при получении staff пользователей: {e}")
                return []
        elif request == 'amount':
            try:
                staff_count = await self.users_collection.count_documents({"STAFF": True})
                logger.info(f"Количество пользователей со статусом STAFF: {staff_count}")
                return staff_count
            except Exception as e:
                logger.error(f"Ошибка при подсчете staff пользователей: {e}")
                return 0
        elif request == 'get_ids':
            try:
                staff_users = []
                async for user in self.users_collection.find(
                    {"STAFF": True},
                    {"USER_ID": 1, "_id": 0}
                ):
                    staff_users.append(user["USER_ID"])
                if not staff_users:
                    logger.warning("Не найдено пользователей со статусом STAFF")
                    return []
                logger.info(f"Получено {len(staff_users)} ID пользователей со статусом STAFF")
                return staff_users
            except Exception as e:
                logger.error(f"Ошибка при получении ID staff пользователей: {e}")
                return []
        else:
            logger.warning(f"Неизвестный запрос: {request}")
            return "Failed! Incorrect request!"

    # --------------- CATEGORY --------------- #

    @async_log_execution_time
    async def create_category(self, name: str, description: str):
        try:
            existing_category = await self.category_collection.find_one({"name": name})
            if existing_category:
                logger.info(f"Категория с именем {name} уже существует")
                return True
            category_data = {
                "NAME": name,
                "DESCRIPTION": description,
                "CREATED_AT": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            result = await self.category_collection.insert_one(category_data)
            logger.info(f"Категория с именем {name} успешно создана")
            return bool(result.inserted_id)
        except Exception as e:
            logger.error(f"Ошибка при создании категории: {e}")
            return False

    @async_log_execution_time
    async def delete_category(self, name: str):
        try:
            result = await self.category_collection.delete_one({"NAME": name})
            success = result.deleted_count > 0
            if success:
                logger.info(f"Категория с именем {name} успешно удалена")
            else:
                logger.warning(f"Категория с именем {name} не найдена")
            return success
        except Exception as e:
            logger.error(f"Ошибка при удалении категории: {e}")
            return False

    @async_log_execution_time
    async def get_all_categories(self):
        try:
            categories = []
            async for category in self.category_collection.find({}):
                categories.append(category)
            if not categories:
                logger.warning("Категории не найдены")
                return []
            logger.info(f"Получено {len(categories)} категорий")
            return categories
        except Exception as e:
            logger.error(f"Ошибка при получении категорий: {e}")
            return []
