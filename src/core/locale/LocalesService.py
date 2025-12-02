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
            "back_to_profile": RuMessages.Profile.BACK_TO_PROFILE,
            "top_up_balance": {
                "top_up_options_stars_button": RuMessages.Profile.TOP_UP_OPTIONS_STARS_BUTTON,
                "top_up_options_crypto_button": RuMessages.Profile.TOP_UP_OPTIONS_CRYPTO_BUTTON,
                "top_up_balance_button": RuMessages.Profile.TOP_UP_BALANCE_BUTTON,
                "top_up_balance_title": RuMessages.Profile.TOP_UP_BALANCE_TITLE,
                "back_to_top_up_balance_button": RuMessages.Profile.BACK_TO_TOP_UP_BALANCE_BUTTON,
            },
            "stars": {
                "input_amount": RuMessages.Profile.Stars.INPUT_AMOUNT,
                "stars_count_error": RuMessages.Profile.Stars.STARS_COUNT_ERROR,
                "pay_stars_button": RuMessages.Profile.Stars.PAY_STARS_BUTTON,
                "title_stars_payment": RuMessages.Profile.Stars.TITLE_STARS_PAYMENT,
                "description_stars_payment": RuMessages.Profile.Stars.DESCRIPTION_STARS_PAYMENT,
                "successful_stars_payment": RuMessages.Profile.Stars.SUCCESSFUL_PAYMENT,
            #TODO Add crypto payment option later
            #"crypto": {
                #"input_amount": RuMessages.Profile.Crypto.INPUT_AMOUNT,
                #"crypto_count_error": RuMessages.Profile.Crypto.CRYPTO_COUNT_ERROR,
                #"pay_crypto_button": RuMessages.Profile.Crypto.PAY_CRYPTO_BUTTON,
                #"title_crypto_payment": RuMessages.Profile.Crypto.TITLE_CRYPTO_PAYMENT,
                #"description_crypto_payment": RuMessages.Profile.Crypto.DESCRIPTION_CRYPTO_PAYMENT,
                #"successful_crypto_payment": RuMessages.Profile.Crypto.SUCCESSFUL_PAYMENT,
            #}
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
            "back_to_profile": EnglishMessages.Profile.BACK_TO_PROFILE,
            "top_up_balance": {
                "top_up_options_stars_button": EnglishMessages.Profile.TOP_UP_OPTIONS_STARS_BUTTON,
                "top_up_options_crypto_button": EnglishMessages.Profile.TOP_UP_OPTIONS_CRYPTO_BUTTON,
                "top_up_balance_button": EnglishMessages.Profile.TOP_UP_BALANCE_BUTTON,
                "top_up_balance_title": EnglishMessages.Profile.TOP_UP_BALANCE_TITLE,
                "back_to_top_up_balance_button": EnglishMessages.Profile.BACK_TO_TOP_UP_BALANCE_BUTTON,
            },
            "stars": {
                "input_amount": EnglishMessages.Profile.Stars.INPUT_AMOUNT,
                "stars_count_error": EnglishMessages.Profile.Stars.STARS_COUNT_ERROR,
                "pay_stars_button": EnglishMessages.Profile.Stars.PAY_STARS_BUTTON,
                "title_stars_payment": EnglishMessages.Profile.Stars.TITLE_STARS_PAYMENT,
                "description_stars_payment": EnglishMessages.Profile.Stars.DESCRIPTION_STARS_PAYMENT,
                "successful_stars_payment": EnglishMessages.Profile.Stars.SUCCESSFUL_PAYMENT,
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

