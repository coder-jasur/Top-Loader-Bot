from src.app.texts import admin_texts


async def lang_getter(lang: str, **_kwargs) -> dict:

    if lang not in admin_texts:
        lang = 'uz'

    return {
        **admin_texts[lang],
        "choose": admin_texts["choose_menu"][lang]
    }
