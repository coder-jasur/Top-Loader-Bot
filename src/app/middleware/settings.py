from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.app.core.config import Settings


class SettingsMiddleware(BaseMiddleware):
    def __init__(self, settings: Settings):
        self._settings = settings

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["settings"] = self._settings
        return await handler(event, data)
