from aiogram import Router, Dispatcher
from aiogram_dialog import Dialog

from src.app.dialogs.admin_menu.menu.dialog import admin_menu_window
from src.app.dialogs.admin_menu.subscription.bots.add_bot.dialog import (
    add_bot_failed, add_bot_pass, add_bot_name,
    add_bot_username
)
from src.app.dialogs.admin_menu.subscription.bots.setup_bot.delete.dialog import (
    on_sure_bot_failed, on_sure_bot_pass,
    delete_bot
)
from src.app.dialogs.admin_menu.subscription.bots.setup_bot.dialog import bot_setup_menu
from src.app.dialogs.admin_menu.subscription.channels.add_channel.dialog import add_channel_dialog

from src.app.dialogs.admin_menu.subscription.channels.setup_channel.channel_message.dialog import \
    (
    add_channel_message_failed, add_channel_message_pass, add_channel_message
)
from src.app.dialogs.admin_menu.subscription.channels.setup_channel.delete.dialog import (
    on_sure_failed, on_sure_pass,
    delete_channel
)
from src.app.dialogs.admin_menu.subscription.channels.setup_channel.dialog import channel_setup_menu
from src.app.dialogs.admin_menu.subscription.dialog import subscription_dialog


def register_subscription_dilaogs(dp: Dispatcher):
    subscription_register_router = Router()

    # add_channel_dialog = Dialog(
    #     subscriptions_menu,
    #     add_channel_window,
    #     add_message_pass,
    #     add_message_failed
    # )
    # setup_channel_dialog = Dialog(
    #     add_channel_message,
    #     add_channel_message_pass,
    #     add_channel_message_failed,
    #     delete_channel,
    #     on_sure_pass,
    #     on_sure_failed,
    #     channel_setup_menu
    # )
    #
    # add_bot_dialog = Dialog(
    #     add_bot_username,
    #     add_bot_name,
    #     add_bot_pass,
    #     add_bot_failed
    # )
    #
    # setup_bot_dialog = Dialog(
    #     delete_bot,
    #     on_sure_bot_pass,
    #     on_sure_bot_failed,
    #     bot_setup_menu
    #
    # )

    subscription_register_router.include_router(admin_menu_window)
    subscription_register_router.include_router(subscription_dialog)
    subscription_register_router.include_router(add_channel_dialog)
    # subscription_register_router.include_router(setup_channel_dialog)
    # subscription_register_router.include_router(add_bot_dialog)
    # subscription_register_router.include_router(setup_bot_dialog)



    dp.include_router(subscription_register_router)