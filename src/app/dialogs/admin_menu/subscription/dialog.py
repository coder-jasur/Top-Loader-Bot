from _operator import itemgetter

from aiogram_dialog import Window, Dialog, StartMode
from aiogram_dialog.widgets.kbd import Select, Row, Button, Group, SwitchTo, Start
from aiogram_dialog.widgets.text import Format, Const

from src.app.dialogs.admin_menu.subscription.getters import subscriptions_menu_getter
from src.app.dialogs.admin_menu.subscription.handlers import on_click_subscription_channel, on_click_subscription_bot
from src.app.states.admin_states import SubscriptionsSG, AdminSG
from src.app.states.channel import AddChannelSG

subscription_dialog = Dialog(
    Window(
        Format("{title}"),
        Group(
            Button(
                Format("{text_channels}"),
                id="channels"
            ),
            Select(
                Format("{item[0]}"),
                id="channel_list",
                item_id_getter=itemgetter(0),
                items="channels",
                on_click=on_click_subscription_channel
            )
        ),
        Group(
            Button(
                Format("{text_bots}"),
                id="bots"
            ),
            Select(
                Format("{item[0]}"),
                id="bots_list",
                item_id_getter=itemgetter(0),
                items="bots",
                on_click=on_click_subscription_bot
            )
        ),
        Row(
            Start(
                Format("{add_channel_text}"),
                id="channel",
                state=AddChannelSG.add_channel,
                mode=StartMode.RESET_STACK
            ),
            SwitchTo(
                Format("{add_bot_text}"),
                id="bot",
                state=SubscriptionsSG.add_bot_username
            )
        ),
        Start(
            text=Format("{back_button_text}"),
            id="back",
            state=AdminSG.menu
        ),
        state=SubscriptionsSG.menu,
        getter=subscriptions_menu_getter
    )
)
