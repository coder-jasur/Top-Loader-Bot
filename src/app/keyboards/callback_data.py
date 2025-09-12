from aiogram.filters.callback_data import CallbackData


class LanguageCD(CallbackData, prefix="language"):
    lang: str
    action: str


class MusicCD(CallbackData, prefix="music"):
    video_id: str


class VideoMusicCD(CallbackData, prefix="videomusic"):
    music_name: str

