from aiogram_dialog import DialogManager

from src.app.texts import admin_texts


async def add_channel_title_getter(dialog_manager: DialogManager, **_):
    lang: str = dialog_manager.middleware_data["lang"]
    title = admin_texts["add_channel_title"][lang]

    return {
        "add_channel_instruction": title,
        "msg_type": dialog_manager.dialog_data.get("msg_type", "start_msg")
    }



async def add_channel_failed_getter(dialog_manager: DialogManager, _):
    lang: str = dialog_manager.middleware_data["lang"]
    failed = admin_texts["failed_add_channel"][lang]
    passed = admin_texts["passed_add_channel"][lang]
    back_kbd_text = admin_texts["back_button"][lang]

    return {"pass": passed,"failed": failed, "back_kbd_text": back_kbd_text}