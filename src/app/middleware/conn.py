from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from asyncpg import Pool


class ConnectionMiddleware(BaseMiddleware):
    def __init__(self, pool: Pool):
        self._pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> None:
        async with self._pool.acquire() as conn:
            data["conn"] = conn
            return await handler(event, data)


