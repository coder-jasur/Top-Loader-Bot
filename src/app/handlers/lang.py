from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from asyncpg import Connection

from src.app.database.queries.users import UserActions
from src.app.keyboards.callback_data import LanguageCD
from src.app.keyboards.inline import language_keyboard_f
from src.app.texts import user_texts

user_language_router = Router()


@user_language_router.callback_query(LanguageCD.filter())
async def modified_user_language(call: CallbackQuery, callback_data: LanguageCD, conn: Connection, lang: str):
    user_actions = UserActions(conn)

    try:
        if callback_data.action == "lang":
            await user_actions.update_user_lang(callback_data.lang, call.from_user.id)
            user_lang = await user_actions.get_user(call.from_user.id)

            await call.message.edit_text(
                text=user_texts["choose_language"][lang],
                reply_markup=language_keyboard_f(user_lang[3])
            )
            return
        if callback_data.action == "check_lang":
            await call.message.edit_text(text=user_texts["start"][lang])
            return

    except Exception as e:
        print(e)



@user_language_router.message(Command("language"))
async def modified_language(message: Message, conn: Connection, lang: str):
    await message.answer(text=user_texts["choose_language"][lang], reply_markup=language_keyboard_f(lang))

