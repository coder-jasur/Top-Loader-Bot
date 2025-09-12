import asyncio
import os
from pprint import pprint

from aiogram.types import Message
from instagrapi import Client
from pydantic.v1.class_validators import all_kwargs

from src.app.core.config import Settings
from src.app.services.audio_music_downloaders import AudioMusicDownloaders
from src.app.services.searchs import Searchs
from src.app.services.utils.files import get_file_name, get_file_name_mp3
from src.app.services.utils.video import download_video
from src.app.services.video_downloaders import VideoDownloaders
from src.app.texts import video_process_texts, music_and_audio_process_texts, photo_process_texts


class AllDownloader:

    def __init__(self, message: Message, lang: str):
        self.message = message
        self.lang = lang
        self.settings = Settings()
        self.video_downloader = VideoDownloaders()
        self.music_downloader = AudioMusicDownloaders()
        self.serch_music = Searchs()

    async def insgtarm_video_music_downloader(self, video_url: str):

        instagram_downloader_errors = []

        video_path = get_file_name()
        audio_path = get_file_name_mp3()
        video_out_path, video_errors = await asyncio.to_thread(
            self.video_downloader.instagram_video_downloader,
            video_url,
            video_path
        )
        music_title, music_errors = await self.music_downloader.find_song_name_by_video(video_out_path, audio_path)

        for video_error in video_errors:
            instagram_downloader_errors.append(video_error)
        for music_error in music_errors:
            instagram_downloader_errors.append(music_error)

        if "error_in_downloading" in instagram_downloader_errors:
            await self.message.edit_text(video_process_texts["error_in_downloading"][self.lang])
        elif "video_file_is_so_big" in instagram_downloader_errors:
            await self.message.edit_text(video_process_texts["video_file_is_so_big"][self.lang])

        elif "music_not_found" in instagram_downloader_errors:
            music_title = None

        return video_out_path, music_title

    async def instagram_stories_music_downloader(self, stories_url: str):
        instagram_downloader_errors = []

        cl = Client()
        cl.login(self.settings.instagram_username, self.settings.instagram_password)

        account_username = stories_url.split("/")[4]
        user_id = await asyncio.to_thread(cl.user_id_from_username, account_username)
        stories = await asyncio.to_thread(cl.user_stories, user_id)

        if not stories:
            instagram_downloader_errors.append("error_in_downloading")
            return None, None

        story_data = None
        for story in stories:
            if story.pk == stories_url.split("/")[5]:
                story_data = story

        stories_path = get_file_name()
        audio_path = get_file_name_mp3()

        story_path = await download_video(str(story_data.video_url),stories_path)

        music_title, music_errors = await self.music_downloader.find_song_name_by_video(story_path, audio_path)

        instagram_downloader_errors.extend(music_errors)

        if "error_in_downloading" in instagram_downloader_errors:
            await self.message.edit_text(video_process_texts["error_in_downloading"][self.lang])
        elif "video_file_is_so_big" in instagram_downloader_errors:
            await self.message.edit_text(video_process_texts["video_file_is_so_big"][self.lang])
        elif "music_not_found" in instagram_downloader_errors:
            music_title = None

        return story_path, music_title

    async def instagram_photo_downloader(self, photo_url: str):
        instagram_downloader_errors = []

        photo_path = get_file_name()
        photo_out_path, photo_errors = await asyncio.to_thread(
            self.video_downloader.instagram_photo_downloader,
            photo_url,
            photo_path,
        )

        for video_error in photo_errors:
            instagram_downloader_errors.append(video_error)


        if "error_in_downloading" in instagram_downloader_errors:
            await self.message.edit_text(photo_process_texts["not_fund"][self.lang])
        elif "photo_file_is_so_big" in instagram_downloader_errors:
            await self.message.edit_text(photo_process_texts["photo_file_is_so_big"][self.lang])

        return photo_out_path

    async def youtube_video_music_downloader(self, video_url: str):
        youtube_downloader_errors = []

        video_path = get_file_name()
        audio_path = get_file_name_mp3()
        video_out_path, video_errors = await asyncio.to_thread(
            self.video_downloader.youtube_video_downloader,
            video_url,
            video_path
        )
        music_title, music_errors = await self.music_downloader.find_song_name_by_video(video_out_path, audio_path)

        for video_error in video_errors:
            youtube_downloader_errors.append(video_error)
        for music_error in music_errors:
            youtube_downloader_errors.append(music_error)

        if "error_in_downloading" in youtube_downloader_errors:
            await self.message.edit_text(video_process_texts["error_in_downloading"][self.lang])
        elif "video_file_is_so_big" in youtube_downloader_errors:
            await self.message.edit_text(video_process_texts["video_file_is_so_big"][self.lang])

        elif "music_not_found" in youtube_downloader_errors:
            music_title = None

        return video_out_path, music_title

    async def tiktok_video_music_downloader(self, video_url: str):
        tiktok_downloader_errors = []

        video_path = get_file_name()
        audio_path = get_file_name_mp3()
        video_out_path, video_errors = await self.video_downloader.tiktok_video_downloader(
            video_url=video_url,
            output_file_name=video_path
        )

        music_title, music_errors = await self.music_downloader.find_song_name_by_video(video_out_path, audio_path)

        for video_error in video_errors:
            tiktok_downloader_errors.append(video_error)

        for music_error in music_errors:
            tiktok_downloader_errors.append(music_error)

        if "error_in_downloading" in tiktok_downloader_errors:
            await self.message.edit_text(video_process_texts["error_in_downloading"][self.lang])
        elif "video_file_is_so_big" in tiktok_downloader_errors:
            await self.message.edit_text(video_process_texts["video_file_is_so_big"][self.lang])

        elif "music_not_found" in tiktok_downloader_errors:
            music_title = None

        return video_out_path, music_title

    async def download_music_from_audio_video_voice(self, message: Message, media_type: str):
        errors = []
        if media_type == "video":
            video_path = get_file_name()
            video = message.video
            file = await message.bot.get_file(video.file_id)

            file_path = file.file_path
            download_path = f"./media/videos/{video_path}"

            await message.bot.download_file(file_path, download_path)

            music_name = await self.music_downloader.find_song_name_by_video_audio_voice(download_path)
            if await asyncio.to_thread(os.path.exists, download_path):
                await asyncio.to_thread(os.remove, download_path)
            if music_name:
                musics_data = await asyncio.to_thread(self.serch_music.search_music, music_name, 5)
            else:
                await self.message.answer(music_and_audio_process_texts["not_found"][self.lang])
                return

            if not music_name or not musics_data:
                errors.append("music_not_found")

            if "music_not_found" in errors:
                await self.message.answer(music_and_audio_process_texts["error_in_downloading"][self.lang])

            musics_list = []
            music_title = ""
            i = 1
            if musics_data:
                for music_data in musics_data:
                    if music_data.get("title"):
                        file_size = music_data.get("filesize_mb")
                        duration = str(music_data.get("duration"))

                        if int(file_size) < 2000 and 10 > int(duration.split(":")[0]):
                            musics_list.append(music_data)
                            music_title += f"{i}. {music_data.get("title")} - {duration}\n\n"
                            i += 1

                return musics_list, music_title
            else:
                await self.message.answer(music_and_audio_process_texts["error_in_downloading"][self.lang])

            return

        elif media_type in ["audio", "voice"]:
            if message.voice:
                audio = message.voice
            else:
                audio = message.audio
            media_path_file = get_file_name_mp3()
            file = await message.bot.get_file(audio.file_id)

            file_path = file.file_path

            download_path = f"./media/audios/{media_path_file}.mp3"
            await message.bot.download_file(file_path, download_path)

            music_name = await self.music_downloader.find_song_name_by_video_audio_voice(download_path)
            if await asyncio.to_thread(os.path.exists, download_path):
                await asyncio.to_thread(os.remove, download_path)

            if not music_name:
                return None

            if music_name:
                musics_data = await asyncio.to_thread(self.serch_music.search_music, music_name, 5)
            else:
                await self.message.answer(music_and_audio_process_texts["not_found"][self.lang])
                return

            if not music_name or not musics_data:
                errors.append("music_not_found")

            if "music_not_found" in errors:
                await self.message.answer(music_and_audio_process_texts["error_in_downloading"][self.lang])
            musics_list = []
            music_title = ""
            i = 1
            if musics_data:
                for music_data in musics_data:
                    if music_data.get("title"):
                        file_size = music_data.get("filesize_mb")
                        duration = str(music_data.get("duration"))

                        if int(file_size) < 2000 and 10 > int(duration.split(":")[0]):
                            musics_list.append(music_data)
                            music_title += f"{i}. {music_data.get("title")} - {duration}\n\n"
                            i += 1
                return musics_list, music_title
            else:
                await self.message.edit_text(music_and_audio_process_texts["error_in_downloading"][self.lang])

            return
        return

    async def download_music_by_avtor_or_music_text(self, music_text_or_avtor: str, max_count: int = 5):
        musics_data = await asyncio.to_thread(self.serch_music.search_music, music_text_or_avtor, max_count)

        musics_list = []
        music_title = ""
        i = 1
        if musics_data:
            for music_data in musics_data:
                if music_data.get("title"):
                    file_size = music_data.get("filesize_mb")
                    duration = str(music_data.get("duration"))

                    if int(file_size) < 2000 and 10 > int(duration.split(":")[0]):
                        musics_list.append(music_data)
                        music_title += f"{i}. {music_data.get("title")} - {duration}\n\n"
                        i += 1
            return musics_list, music_title
        else:
            await self.message.edit_text(music_and_audio_process_texts["error_in_downloading"][self.lang])

        return

    async def download_music_from_youtube(self, video_id: str):
        music_path = get_file_name_mp3()
        music_output_path, title = await asyncio.to_thread(
            self.music_downloader.download_music_from_youtube,
            f"https://www.youtube.com/watch?v={video_id}",
            music_path
        )

        if not title:
            await self.message.answer(music_and_audio_process_texts["not_found"][self.lang])

        return music_output_path, title
