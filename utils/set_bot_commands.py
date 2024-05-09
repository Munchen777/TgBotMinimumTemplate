from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeDefault,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllPrivateChats
)

from typing import Never


async def set_commands(bot: Bot) -> Never:
    await set_private_commands(bot)


async def set_private_commands(bot: Bot):
    private_commands = {
        "ru": [
            BotCommand(command="start", description="Старт бота")
        ],
        "en": [
            BotCommand(command="start", description="Start bot")
        ]
    }

    for lang_code, commands in private_commands.items():
        return await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeAllPrivateChats(),
            language_code=lang_code
        )
