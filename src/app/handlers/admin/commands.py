from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from asyncpg import Connection

from src.app.database.queries.bots import BotActions
from src.app.database.queries.channels import ChannelActions
from src.app.keyboards.inline import back_to_subscriptions_menu_button
from src.app.states.admin_states import AdminSG, AddSubscriptionsSG, SubscriptionsSG
from src.app.texts import admin_texts

admin_commands_router = Router()


@admin_commands_router.message(Command("admin_menu"))
async def main_admin_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminSG.menu)


@admin_commands_router.callback_query(F.data == "back_to_subscriptions_menu")
async def back_to_subscriptionst_menu_handle(call: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.switch_to(SubscriptionsSG.menu)

