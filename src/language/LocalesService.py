from resources.locales.ru import Messages as RuMessages
from resources.locales.en import Messages as EnglishMessages

"""
@author Nik/diplexion
@project TeleCommerce
@date 01/12/2025
"""

LOCALES = {
    "ru-RU": {
        "welcome": RuMessages.WELCOME_MSG,
        "language_selected": RuMessages.LANGUAGE_SELECTED,
        "language_selection": RuMessages.LANGUAGE_SELECTION,
        "russian": RuMessages.RUSSIAN,
        "english": RuMessages.ENGLISH,
        "info": RuMessages.INFO,
        "profile": {
            "profile_main": RuMessages.Profile.MAIN,
            "top_up_balance": RuMessages.Profile.TOP_UP_BALANCE,
            "stars": {
                "input_amount": RuMessages.Profile.Stars.INPUT_AMOUNT,
                "stars_count_error": RuMessages.Profile.Stars.STARS_COUNT_ERROR,
                "pay_stars_button": RuMessages.Profile.Stars.PAY_STARS_BUTTON,
            },
        },
        "store": {
            "store_main": RuMessages.Store.STORE_MAIN,
        },
        "error": RuMessages.ERROR,
        "profile_created": RuMessages.PROFILE_CREATED,
    },
    "en-US": {
        "welcome": EnglishMessages.WELCOME_MSG,
        "language_selected": EnglishMessages.LANGUAGE_SELECTED,
        "language_selection": EnglishMessages.LANGUAGE_SELECTION,
        "russian": EnglishMessages.RUSSIAN,
        "english": EnglishMessages.ENGLISH,
        "info": EnglishMessages.INFO,
        "profile": {
            "profile_main": EnglishMessages.Profile.MAIN,
            "top_up_balance": EnglishMessages.Profile.TOP_UP_BALANCE,
            "stars": {
        #     "input_amount":  EnglishMessages.Profile.INPUT_AMOUNT,
            },
        },
        "store": {
            "store_main": EnglishMessages.Store.STORE_MAIN,
        },
        "error": EnglishMessages.ERROR,
        "profile_created": EnglishMessages.PROFILE_CREATED,
    }
}


def get_text(key: str, locale: str = "ru-RU", **kwargs) -> str:
    if locale not in LOCALES:
        locale = "ru-RU"

    parts = key.split(".")
    node = LOCALES[locale]

    for part in parts:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            node = None
            break

    if node is None:
        node = LOCALES[locale].get(key, key)

    text = node if isinstance(node, str) else key

    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass

    return text

