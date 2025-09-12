from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.states.admin_states import ChannelSG


async def on_sure(call: CallbackQuery, _, dialog_manager: DialogManager):
    channel_id = dialog_manager.dialog_data.get("channel_id")
    conn: Connection = dialog_manager.middleware_data["conn"]

    try:
        channel_actions = ChannelActions(conn)
        await channel_actions.delete_channel(channel_id)

        await dialog_manager.switch_to(ChannelSG.delete_sure_pass)
    except Exception as e:
        print("Error", e)
        await dialog_manager.switch_to(ChannelSG.delete_sure_failed)




