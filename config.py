from os import getenv

class Config:
    # List of available bot commands on the quick access toolbar
    Commands = ["info", "store", "profile", "help"]
    class Stars:
        # In rubles by default. Like 1 star = 1.3 rubles
        EXCHANGE_RATE = 1.3
    class Database:
        # "TeleCommerce" by default
        DB_NAME = getenv("DB_NAME")

        # "mongodb://localhost:27017" by default
        MONGO_URI = getenv('MONGO_URI')

        # "users" by default
        USER_COLLECTION_NAME = getenv("USER_COLLECTION_NAME")