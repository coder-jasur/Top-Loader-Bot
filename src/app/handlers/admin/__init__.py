from aiogram import Router, F

from src.app.core.config import Settings
from src.app.handlers.admin.commands import admin_commands_router


def register_admin_routers(router: Router, settings: Settings):
    admins_id = []
    for admin in settings.admins_ids:
        admins_id.append(int(admin))
    admir_register_router = Router()
    admir_register_router.message.filter(F.from_user.id.in_(admins_id))
    admir_register_router.callback_query.filter(F.from_user.id.in_(admins_id))
    admir_register_router.include_router(admin_commands_router)
    router.include_router(admir_register_router)