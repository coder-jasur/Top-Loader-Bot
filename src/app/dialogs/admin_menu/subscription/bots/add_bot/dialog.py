from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, SwitchTo
from aiogram_dialog.widgets.text import Format

from src.app.dialogs.admin_menu.subscription.bots.add_bot.funcktions import add_bot, get_bot_username
from src.app.dialogs.admin_menu.subscription.bots.add_bot.getters import bot_add_dialog_text_getter, add_result_getter
from src.app.states.admin_states import SubscriptionsSG

add_bot_username = Window(
    Format("{get_bot_username}"),
    MessageInput(
        func=get_bot_username,
        content_types=ContentType.TEXT
    ),
    getter=bot_add_dialog_text_getter,
    state=SubscriptionsSG.add_bot_username
)

add_bot_name = Window(
    Format("{get_bot_name}"),
    MessageInput(
        func=add_bot,
        content_types=ContentType.TEXT
    ),
    getter=bot_add_dialog_text_getter,
    state=SubscriptionsSG.add_bot_name
)


add_bot_pass = Window(
    Format("{pass}"),
    Row(
        SwitchTo(
            Format("{back_kbd_text}"),
            id="back_to_subscriptions_menu",
            state=SubscriptionsSG.menu
        )
    ),
    state=SubscriptionsSG.add_bot_pass,
    getter=add_result_getter
)

add_bot_failed = Window(
    Format("{failed}"),
    Row(
        SwitchTo(
            Format("{back_kbd_text}"),
            id="back_to_subscriptions_menu",
            state=SubscriptionsSG.menu
        )
    ),
    state=SubscriptionsSG.add_bot_failed,
    getter=add_result_getter
)
