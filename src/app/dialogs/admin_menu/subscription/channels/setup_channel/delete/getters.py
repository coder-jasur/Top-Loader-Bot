from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.texts import admin_texts


async def delete_channel_text_getter(dialog_manager: DialogManager, _):
    conn: Connection = dialog_manager.middleware_data["conn"]
    lang: str = dialog_manager.middleware_data["lang"]
    channel_id = dialog_manager.dialog_data.get("channel_id")

    channel_actions = ChannelActions(conn)

    channel_data = await channel_actions.get_channel(channel_id)

    title = admin_texts["are_you_sure"][lang].format(channel_data[1])

    return {
        "sure": admin_texts["sure"][lang],
        "not_sure": admin_texts["not_sure"][lang],
        "title": title

    }

async def delete_text_getter_pass(dialog_manager: DialogManager, _):
    lang: str = dialog_manager.middleware_data["lang"]

    title = admin_texts["pased_delete_channel"][lang]
    back_kbd_text = admin_texts["back_button"][lang]

    return {"title": title, "back_kbd_text": back_kbd_text}


async def delete_text_getter_failed(dialog_manager: DialogManager, _):
    lang: str = dialog_manager.middleware_data["lang"]

    title = admin_texts["failed_delete_channel"][lang]
    back_kbd_text = admin_texts["back_button"][lang]

    return {"title": title, "back_kbd_text": back_kbd_text}





