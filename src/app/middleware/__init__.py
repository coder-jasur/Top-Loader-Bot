import asyncpg
from aiogram import Dispatcher

from src.app.core.config import Settings
from src.app.middleware.conn import ConnectionMiddleware
from src.app.middleware.language import LanguageMiddleware
from src.app.middleware.settings import SettingsMiddleware


def register_middleware(dp: Dispatcher, pool: asyncpg.Pool, settings_: Settings):

    connection_middleware = ConnectionMiddleware(pool)
    dp.message.outer_middleware(connection_middleware)
    dp.callback_query.outer_middleware(connection_middleware)

    language_middleware = LanguageMiddleware()
    dp.message.outer_middleware(language_middleware)
    dp.callback_query.outer_middleware(language_middleware)
    dp.chat_member.outer_middleware(language_middleware)

    settings_middleware = SettingsMiddleware(settings_)
    dp.message.outer_middleware(settings_middleware)
    dp.callback_query.outer_middleware(settings_middleware)
    dp.chat_member.outer_middleware(settings_middleware)
