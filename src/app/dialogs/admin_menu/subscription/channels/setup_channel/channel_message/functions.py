from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.states.admin_states import ChannelSG


async def add_channel_message_func(message: Message, _, dialog_manager: DialogManager):
    conn: Connection = dialog_manager.middleware_data["conn"]
    channel_id = dialog_manager.dialog_data.get("channel_id")
    try:
        channel_actions = ChannelActions(conn)

        await channel_actions.add_channel_message(channel_id, message.text)
        await dialog_manager.switch_to(ChannelSG.add_channel_message_pass)

    except Exception as e:
        print("Error", e)
        await dialog_manager.switch_to(ChannelSG.add_channel_message_failed)