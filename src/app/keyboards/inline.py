from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.app.keyboards.callback_data import LanguageCD, MusicCD, VideoMusicCD
from src.app.texts import user_texts, admin_texts, music_and_audio_process_texts


def language_keyboard_f(language: str) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardBuilder()

    if language == "uz":
        buttons.row(
            InlineKeyboardButton(text="🇺🇿 O'zbekcha ✅", callback_data=LanguageCD(lang="uz", action="modified").pack())
        )
        buttons.row(
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data=LanguageCD(lang="ru", action="lang").pack())
        )
        buttons.row(
            InlineKeyboardButton(text="🇺🇸 English", callback_data=LanguageCD(lang="en", action="lang").pack())
        )
    elif language == "ru":
        buttons.row(
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data=LanguageCD(lang="uz", action="lang").pack())
        )
        buttons.row(
            InlineKeyboardButton(text="🇷🇺 Русский ✅", callback_data=LanguageCD(lang="ru", action="modified").pack())
        )
        buttons.row(
            InlineKeyboardButton(text="🇺🇸 English", callback_data=LanguageCD(lang="en", action="lang").pack())
        )
    elif language == "en":
        buttons.row(
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data=LanguageCD(lang="uz", action="lang").pack())
        )
        buttons.row(
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data=LanguageCD(lang="ru", action="lang").pack())
        )
        buttons.row(
            InlineKeyboardButton(text="🇺🇸 English ✅", callback_data=LanguageCD(lang="en", action="modified").pack())
        )

    buttons.row(InlineKeyboardButton(text="✅", callback_data=LanguageCD(lang="none", action="check_lang").pack()))

    return buttons.as_markup()


def video_keyboards(music_name: str, lang: str):
    buttons = InlineKeyboardBuilder()

    buttons.row(
        InlineKeyboardButton(
            text=music_and_audio_process_texts["download_is"][lang],
            callback_data=VideoMusicCD(
                music_name=music_name[:30],
            ).pack()
        )
    )
    return buttons.as_markup()


def music_keyboards(music_list: list):
    buttons_builder = InlineKeyboardBuilder()
    i = 0

    for music in music_list:
        i += 1
        buttons_builder.add(
            InlineKeyboardButton(
                text=str(i),
                callback_data=MusicCD(
                    video_id=music.get("id")[:30]
                ).pack()
            )
        )

    buttons_builder.row(
        InlineKeyboardButton(
            text="❌",
            callback_data="delete_list_music"
        )
    )
    return buttons_builder.as_markup()


def back_to_subscriptions_menu_button(lang: str):
    buttons = InlineKeyboardBuilder()

    buttons.row(
        InlineKeyboardButton(
            text=admin_texts["back_button"][lang],
            callback_data="back_to_subscriptions_menu"
        )
    )
    return buttons.as_markup()

