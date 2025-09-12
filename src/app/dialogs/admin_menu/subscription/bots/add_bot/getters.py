from aiogram_dialog import DialogManager

from src.app.texts import admin_texts


async def bot_add_dialog_text_getter(dialog_manager: DialogManager, _):
    lang: str = dialog_manager.middleware_data["lang"]
    get_username_title = admin_texts["get_bot_username"][lang]
    get_name_title =admin_texts["get_bot_name"][lang]

    return {"get_bot_username": get_username_title, "get_bot_name": get_name_title}




async def add_result_getter(dialog_manager: DialogManager, _):
    lang: str = dialog_manager.middleware_data["lang"]
    passed = admin_texts["passed_add_channel"][lang]
    failed = admin_texts["failed_add_channel"][lang]
    back_kbd_text = admin_texts["back_button"][lang]

    return {"pass": passed, "failed": failed, "back_kbd_text": back_kbd_text}

