from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.texts import admin_texts


async def channel_data_getter(dialog_manager: DialogManager, _):
    channel_id = dialog_manager.start_data.get("channel_id")
    conn: Connection = dialog_manager.middleware_data["conn"]
    lang: str = dialog_manager.middleware_data["lang"]
    channel_actions = ChannelActions(conn)

    channel_data = await channel_actions.get_channel(int(channel_id))
    bot_status = admin_texts["mandatoriy_subscription"][channel_data[3]][lang]


    title = admin_texts["channel_info_text"][lang].format(
        channel_data[0],
        channel_data[1],
        channel_data[2],
        bot_status,
        channel_data[2]
    )

    if channel_data[3] == "True":
        msb = admin_texts["delete_from_mandatory"][lang]
    else:
        msb = admin_texts["add_to_mandatory"][lang]

    delite_message = None

    if channel_data[-2]:
        delite_message = "🗑"

    return {
        "title": title,
        "setup_mandatory_subscription_kbd_text": msb,
        "delite_channel_button_kbd_text": admin_texts["delete_channel"][lang],
        "back_to_subscriptions_menu_kbd_text": admin_texts["back_button"][lang],
        "add_channel_message_kbd_text": admin_texts["add_channel_message_button"][lang],
        "delite_channel_message_kbd_text": delite_message
    }
