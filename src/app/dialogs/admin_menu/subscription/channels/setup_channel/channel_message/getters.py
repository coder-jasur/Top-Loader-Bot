from aiogram_dialog import DialogManager

from src.app.texts import admin_texts


async def add_channel_mesage_title_getter(dialog_manager: DialogManager, _):
    lang: str = dialog_manager.middleware_data["lang"]

    title = admin_texts["add_channel_title"][lang]

    return {"title": title}


async def add_message_pass_getter(dialog_manager: DialogManager, _):
    lang: str = dialog_manager.middleware_data["lang"]

    title = admin_texts["channel_message_success"][lang]

    return {"title": title}

async def add_message_failed_getter(dialog_manager: DialogManager, _):
    lang: str = dialog_manager.middleware_data["lang"]

    title = admin_texts["channel_message_error"][lang]

    return {"title": title}

