import asyncio
import os

from shazamio import Shazam
from yt_dlp import YoutubeDL
from src.app.services.utils.audio import extract_audio_from_video


class AudioMusicDownloaders:
    def __init__(self):
        self.shazam = Shazam()

    def download_music_from_youtube(self, video_url: str, music_path: str):

        music_output_path = f"./media/audios/{music_path}"

        yt_dlp_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': music_output_path,
            'default_search': 'ytsearch1:',
            'quiet': True,
            'no_warnings': True,
        }


        with YoutubeDL(yt_dlp_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info["entries"][0]["title"] if "entries" in info else info["title"]

        return music_output_path + ".mp3", title

    async def find_song_name_by_video_audio_voice(self, media_path: str):

        out = await self.shazam.recognize(media_path)
        track = out.get("track", {})
        title = track.get("title", "")
        subtitle = track.get("subtitle", "")
        music_title = f"{title} {subtitle}".strip()


        return music_title

    async def find_song_name_by_video(self, video_path: str, audio_path: str):
        audio_path_file = f"./media/audios/{audio_path}.mp3"

        audio_path = await asyncio.to_thread(extract_audio_from_video, video_path, audio_path_file)

        try:
            if audio_path:
                out = await self.shazam.recognize(audio_path_file)
                track = out.get("track", {})
                title = track.get("title", "")
                subtitle = track.get("subtitle", "")
                music_title = f"{title} {subtitle}".strip()

                if audio_path:
                    if await asyncio.to_thread(os.path.exists, audio_path):
                        await asyncio.to_thread(os.remove, audio_path_file)

                errors = []
                if not music_title:
                    errors.append("music_not_found")

                return music_title, errors

        except Exception as e:
            print(f"ERROR", e)
            return None
