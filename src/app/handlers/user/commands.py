from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.app.texts import user_texts

user_commands_router = Router()

@user_commands_router.message(Command("about"))
async def handled_command_about(message: Message, lang: str):
    await message.answer(user_texts["about"][lang])