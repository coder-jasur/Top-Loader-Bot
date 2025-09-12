from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Button, SwitchTo
from aiogram_dialog.widgets.text import Format

from src.app.dialogs.admin_menu.subscription.channels.setup_channel.getters import channel_data_getter
from src.app.dialogs.admin_menu.subscription.channels.setup_channel.handlers import (
        on_click_mandatory_subscription,
        on_delete_channel_message
)
from src.app.states.admin_states import ChannelSG, SubscriptionsSG

channel_setup_menu = Window(
    Format("{title}"),
    Group(
        SwitchTo(
            text=Format("{delite_channel_button_kbd_text}"),
            id="delite_channel",
            state=ChannelSG.delete_channel
        ),
        Button(
            Format("{setup_mandatory_subscription_kbd_text}"),
            id="setup_mandatory_subscription",
            on_click=on_click_mandatory_subscription
        ),
        SwitchTo(
            Format("add_channel_message_kbd_text"),
            id="add_channel_message",
            state=ChannelSG.add_channel_message
        ),
        Button(
            Format("{delite_channel_message_kbd_text}"),
            id="delite_channel_message",
            on_click=on_delete_channel_message
        ),
        SwitchTo(
            Format("{back_to_subscriptions_menu_kbd_text}"),
            id="back_to_subscriptions_menu",
            state=SubscriptionsSG.menu
        ),
        width=2
    ),
    state=ChannelSG.channel_setup_menu,
    getter=channel_data_getter
)
