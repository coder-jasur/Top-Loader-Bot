from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.app.states.admin_states import ChannelSG, BotSG


async def on_click_subscription_channel(
    call: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str
):
    dialog_manager.dialog_data["channel_id"] = int(item_id)
    await dialog_manager.switch_to(ChannelSG.channel_setup_menu)

async def on_click_subscription_bot(
    call: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str
):
    dialog_manager.dialog_data["bot_username"] = item_id
    await dialog_manager.switch_to(BotSG.bot_setup_menu)





