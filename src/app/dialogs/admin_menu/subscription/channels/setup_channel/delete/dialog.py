from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Format

from src.app.dialogs.admin_menu.subscription.channels.setup_channel.delete.getters import (
    delete_channel_text_getter, delete_text_getter_pass, delete_text_getter_failed,
)
from src.app.dialogs.admin_menu.subscription.channels.setup_channel.delete.handlers import on_sure
from src.app.states.admin_states import ChannelSG, SubscriptionsSG

delete_channel = Window(
    Format("{title}"),
    Row(
        Button(
            Format("{sure}"),
            id="sure",
            on_click=on_sure
        ),
        SwitchTo(
            Format("{no}"),
            id="no",
            state=ChannelSG.channel_setup_menu
        )
    ),
    state=ChannelSG.delete_channel,
    getter=delete_channel_text_getter

)

on_sure_pass = Window(
    Format("{title}"),
    Row(
        SwitchTo(
            Format("{back_kbd_text}"),
            id="back_to_subscriptions_menu",
            state=SubscriptionsSG.menu
        )
    ),
    state=ChannelSG.delete_sure_pass,
    getter=delete_text_getter_pass
)

on_sure_failed = Window(
    Format("{title}"),
    Row(
        SwitchTo(
            Format("{back_kbd_text}"),
            id="back_to_subscriptions_menu",
            state=ChannelSG.channel_setup_menu
        )
    ),
    state=ChannelSG.delete_sure_failed,
    getter=delete_text_getter_failed
)
