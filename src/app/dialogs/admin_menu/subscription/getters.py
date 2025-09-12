from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.database.queries.bots import BotActions
from src.app.database.queries.channels import ChannelActions
from src.app.texts import admin_texts


async def subscriptions_menu_getter(dialog_manager: DialogManager, **_) -> dict:
    conn: Connection = dialog_manager.middleware_data["conn"]
    lang: str = dialog_manager.middleware_data["lang"]
    bot_actions = BotActions(conn)
    channel_actions = ChannelActions(conn)

    bots_info = await bot_actions.get_all_bots()
    channels_info = await channel_actions.get_all_channels()

    title = admin_texts[lang]["setup_bot"]

    if not bots_info and not channels_info:
        title = admin_texts["none_menu_subscriptions"][lang]

    return {
        "title": title,
        "channels": [(c[0], c[1]) for c in channels_info],
        "bots": [(b[0], b[1]) for b in bots_info],
        "add_channel_text": admin_texts["add_channel"][lang],
        "add_bot_text": admin_texts["add_bot"][lang],
        "back_button_text": admin_texts["back_button"][lang],
        "text_channels": admin_texts["setup_bot"][lang] if channels_info else "",
        "text_bots": admin_texts["bots"][lang] if bots_info else ""
    }


