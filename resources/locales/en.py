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

    # You can edit the info command message here, although I'd appreciate it if you didn't
    INFO = """
🤖 *About the bot*  

*Version:* `1.0`  
*Supported languages:* Russian, English  
*Author:* [diplexion](https://github.com/diplexion) 
*Last update date:* 2025-12-01  
*Source code:* [SourceCode]()
    """

    ERROR = "❌ An error occurred. Please contact support."
    PROFILE_CREATED = "✅ Profile successfully created!"

    class Profile:
        MAIN = """
👤 *Your profile:*

🆔 {id}
👨‍💻 {language}
💰 *Balance:* {balance}

📅 *Registration date:* {registration_date}
            """

        TOP_UP_BALANCE = "💳 Top up balance"

    class Store:
        STORE_MAIN = """
🏬 *TeleCommerce Store*

Select a product category:    
        """
