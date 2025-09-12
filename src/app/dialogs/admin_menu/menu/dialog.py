from aiogram_dialog import Window, StartMode, Dialog
from aiogram_dialog.widgets.kbd import Group, Button, Start
from aiogram_dialog.widgets.text import Format

from src.app.dialogs.admin_menu.menu.getters import lang_getter

from src.app.states.admin_states import AdminSG, SubscriptionsSG

admin_menu_window = Dialog(
    Window(
        Format("{choose}"),
        Group(
            Start(
                Format("{setup_bot}"),
                id="setup_bot",
                state=SubscriptionsSG.menu,
                mode=StartMode.RESET_STACK
            ),
            Button(Format("{referrals}"), id="referrals"),
            Button(Format("{statistics}"), id="statistics"),
            Button(Format("{broadcast}"), id="broadcast"),
            Button(Format("{user_management}"), id="user_management"),
            Button(Format("{admins_management}"), id="admins_management"),
            Button(Format("{quit}"), id="quit"),
            width=2,
        ),
        getter=lang_getter,
        state=AdminSG.menu,
    )
)
