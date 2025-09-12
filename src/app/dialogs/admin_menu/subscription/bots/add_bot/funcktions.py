from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from asyncpg import Connection

from src.app.database.queries.bots import BotActions
from src.app.states.admin_states import SubscriptionsSG


async def get_bot_username(_, text: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["bot_username"] = text
    await dialog_manager.switch_to(SubscriptionsSG.add_bot_name)



async def add_bot(_, text: MessageInput, dialog_manager: DialogManager) -> None:
    conn: Connection = dialog_manager.middleware_data["conn"]

    try:
        bot_actions = BotActions(conn)
        bot_name = text
        bot_username = dialog_manager.dialog_data.get("bot_username")

        await bot_actions.add_bot(str(bot_name), bot_username)

        await dialog_manager.switch_to(SubscriptionsSG.add_bot_pass)

    except Exception as e:
        print("Add bot error:", e)
        await dialog_manager.switch_to(SubscriptionsSG.add_bot_failed)