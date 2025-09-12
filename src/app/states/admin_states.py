from aiogram.fsm.state import StatesGroup, State


class AdminSG(StatesGroup):
    menu = State()


class SubscriptionsSG(StatesGroup):
    menu = State()

    # channel_modified_menu = State()
    # bot_modifie_menu = State()

    add_channel = State()
    add_channel_pass = State()
    add_channel_failed = State()

    add_bot_username = State()
    add_bot_name = State()
    add_bot_pass = State()
    add_bot_failed = State()


class ChannelSG(StatesGroup):
    options = State()
    channel_setup_menu = State()
    delete_channel = State()
    delete_sure_pass = State()
    delete_sure_failed = State()
    add_channel_message = State()
    add_channel_message_pass = State()
    add_channel_message_failed = State()



class BotSG(StatesGroup):
    bot_setup_menu = State()
    delete_bot = State()
    delete_sure_pass = State()
    delete_sure_failed = State()

class AddSubscriptionsSG(StatesGroup):
    get_channel_id = State()
    get_bot_username = State()
    get_bot_name = State()