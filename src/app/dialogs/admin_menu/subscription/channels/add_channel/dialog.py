from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, SwitchTo
from aiogram_dialog.widgets.text import Format, Case

from src.app.dialogs.admin_menu.subscription.channels.add_channel.funcktions import add_channel
from src.app.dialogs.admin_menu.subscription.channels.add_channel.getters import (
    add_channel_title_getter,
    add_channel_failed_getter
)
from src.app.states.admin_states import SubscriptionsSG
from src.app.states.channel import AddChannelSG

add_channel_dialog = Dialog(
    Window(
        Case(
            {
                "start_msg": Format("{add_channel_instruction}"),
                "not_forwarded": Format("Notugri format, siz pereslat qilishingiz kerak"),
            },
            selector="msg_type"
        ),
        MessageInput(
            func=add_channel,
            content_types=ContentType.TEXT
        ),
        getter=add_channel_title_getter,
        state=AddChannelSG.add_channel
    )
)
