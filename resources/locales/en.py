"""
All messages in the bot are formatted using Markdown.

https://core.telegram.org/bots/api#formatting-options
"""

class Messages:
    WELCOME_MSG = "👋 Welcome, {name}!"
    LANGUAGE_SELECTED = "✅ Language set to English"
    LANGUAGE_SELECTION = "🌐 Language selection"
    RUSSIAN = "🇷🇺 Russian"
    ENGLISH = "🇬🇧 English"

    # You can edit the bot info message here, although I would appreciate it if you don't.
    INFO = """
🤖 *About the bot*  

*Version:* `1.0`  
*Supported languages:* Russian, English  
*Author:* [diplexion](https://github.com/diplexion) 
*Last update:* 2025-12-01  
*Source code:* [SourceCode](https://github.com/diplexion/TeleCommerce)
    """

    ERROR = "❌ An error occurred. Please contact support."
    PROFILE_CREATED = "✅ Profile successfully created!"

    class Profile:
        MAIN = """
👤 *User Profile*

*Name:* `{user_name}`  
*ID:* `{id}`  
*Language:* `{language}`

*Balance:* `{balance}₽`  
*Active bonuses:* `0` (In development)

📅 *Registered:* `{registration_date}`

🎟 *Referral code:* `` (In development)
            """

        BACK_TO_PROFILE = "🔙 Back to profile"

        TOP_UP_BALANCE_BUTTON = "💳 Top up balance"

        TOP_UP_BALANCE_TITLE = """
*💳 Top Up Balance*

Choose a payment method:

• ⭐ *Telegram Stars* — instant top-up  
• 🪙 *Crypto* — convenient cryptocurrency payment

Click on the option below 👇
        """

        TOP_UP_OPTIONS_CRYPTO_BUTTON = "💠 Crypto (In development)"

        TOP_UP_OPTIONS_STARS_BUTTON = "⭐️ Telegram Stars"

        BACK_TO_TOP_UP_BALANCE_BUTTON = "🔙 Back to payment options"

        class Stars:
            INPUT_AMOUNT = """
*⭐ Top up via Telegram Stars*

Current rate: *1 ⭐ = {exchange_rate} ₽*

Enter the number of stars you want to use to top up your balance:

        """

            STARS_COUNT_ERROR = "❌ Please enter a valid number of stars."
            PAY_STARS_BUTTON = "Pay ⭐️"
            TITLE_STARS_PAYMENT = "Balance top-up via TG Stars"
            DESCRIPTION_STARS_PAYMENT = "Balance top-up via TG Stars: {amount} ⭐️"
            SUCCESSFUL_PAYMENT = """
⭐ *Payment via Telegram Stars was successful!*

You paid: *{stars} ⭐*
Credited to balance: *{rubles} ₽*
Your new balance: *{new_balance} ₽*

Payment method: _Telegram Stars_
Transaction ID: `{transaction_id}`
Transaction date: `{date}`

Thank you, {user_name}!  
If you have any questions, contact support: {support_contact}
            """

    class Store:
        STORE_MAIN = """
🏬 *TeleCommerce Store*

Select a product category:    
        """

