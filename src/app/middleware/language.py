from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from asyncpg import Connection

from src.app.database.queries.users import UserActions



class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ):
        conn: Connection = data["conn"]
        user_actions = UserActions(conn=conn)
        user_data = await user_actions.get_user(event.from_user.id)

        lang = event.from_user.language_code
        if not user_data:
            if event.from_user.language_code in ["en", "ru", "uz"]:
                await user_actions.add_user(
                    tg_id=event.from_user.id,
                    username=event.from_user.username or event.from_user.first_name,
                    language=lang
                )
                data["lang"] = lang
                return await handler(event, data)
            else:
                await user_actions.add_user(
                    tg_id=event.from_user.id,
                    username=event.from_user.username or event.from_user.first_name,
                    language="uz"
                )
                data["lang"] = "uz"
                return await handler(event, data)

        data["lang"] = user_data[3]
        return await handler(event, data)



