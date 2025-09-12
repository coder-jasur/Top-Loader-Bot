from aiogram.types import Message
from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.keyboards.inline import back_to_subscriptions_menu_button
from src.app.states.admin_states import SubscriptionsSG
from src.app.texts import admin_texts


async def add_channel(message: Message, _, manager: DialogManager) -> None:
    conn: Connection = manager.middleware_data["conn"]

    if not message.forward_from_chat:
        return await manager.update({"msg_type": "not_forwarded"})

    try:
        channel_actions = ChannelActions(conn)
        channel_name = message.forward_from_chat.full_name
        channel_id = message.forward_from_chat.id
        channel_username = message.forward_from_chat.username

        await channel_actions.add_channel(channel_id, channel_name, channel_username)

        await manager.switch_to(SubscriptionsSG.add_channel_pass)

    except Exception as e:
        print("Add channel error:", e)
        await manager.switch_to(SubscriptionsSG.add_channel_failed)

