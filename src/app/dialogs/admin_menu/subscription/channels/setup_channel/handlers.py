from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.dialogs.admin_menu.subscription.channels.setup_channel.getters import channel_data_getter
from src.app.texts import admin_texts


async def on_click_mandatory_subscription(call: CallbackQuery, _, dialog_manager: DialogManager):
    conn: Connection = dialog_manager.middleware_data["conn"]
    lang: str = dialog_manager.middleware_data["lang"]
    channel_id = dialog_manager.dialog_data.get("channel_id")
    channel_actions = ChannelActions(conn)
    channel_data = await channel_actions.get_channel(channel_id)
    if channel_data[3] == "True":
        await channel_actions.update_channel_status("False", channel_id)
    elif channel_data[3] == "False":
        await channel_actions.update_channel_status("True", channel_id)
    else:
        await call.answer(admin_texts["error_mandatoriy_subscription"][lang])

    data = await channel_data_getter(dialog_manager, _)

    await dialog_manager.update(data)


async def on_delete_channel_message(call: CallbackQuery, _, dialog_manager: DialogManager):
    conn: Connection = dialog_manager.middleware_data["conn"]
    lang: str = dialog_manager.middleware_data["lang"]
    channel_id = dialog_manager.dialog_data.get("channel_id")
    channel_actions = ChannelActions(conn)
    try:
        await channel_actions.delete_channel_message(channel_id)
        await call.answer(admin_texts["passed_message_delete"][lang])
    except Exception as e:
        print("Error", e)
        await call.answer(admin_texts["failed_message_delete"][lang])