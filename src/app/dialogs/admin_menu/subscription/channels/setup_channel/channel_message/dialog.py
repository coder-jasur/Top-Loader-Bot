from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, SwitchTo
from aiogram_dialog.widgets.text import Format

from src.app.dialogs.admin_menu.subscription.channels.setup_channel.channel_message.functions import \
    add_channel_message_func
from src.app.dialogs.admin_menu.subscription.channels.setup_channel.channel_message.getters import \
    (
    add_channel_mesage_title_getter, add_message_pass_getter, add_message_failed_getter
)
from src.app.states.admin_states import ChannelSG

add_channel_message = Window(
    Format("{title}"),
    MessageInput(
        func=add_channel_message_func,
        content_types=ContentType.TEXT
    ),
    state=ChannelSG.add_channel_message,
    getter=add_channel_mesage_title_getter
)


add_channel_message_pass = Window(
    Format("{title}"),
    Row(
        SwitchTo(
            Format("{back_kbd_text}"),
            id="back_to_subscriptions_menu",
            state=ChannelSG.channel_setup_menu
        )
    ),
    state=ChannelSG.add_channel_message_pass,
    getter=add_message_pass_getter
)

add_channel_message_failed = Window(
    Format("{title}"),
    Row(
        SwitchTo(
            Format("{back_kbd_text}"),
            id="back_to_subscriptions_menu",
            state=ChannelSG.channel_setup_menu
        )
    ),
    state=ChannelSG.add_channel_message_failed,
    getter=add_message_failed_getter
)


