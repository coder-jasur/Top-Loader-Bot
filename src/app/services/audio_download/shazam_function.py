import asyncio
import logging
import os
import time

import yt_dlp
from aiogram.types import Message
from shazamio import Shazam
from yt_dlp import YoutubeDL

from src.app.common.file.audio import extract_audio_from_video

logging.basicConfig(level=logging.INFO)


def search_youtube(query: str, limit: int = 5):
    ydl_opts = {
        "quiet": True,
        "match_filter": yt_dlp.utils.match_filter_func("duration < 600"),
        "skip_download": True,
    }

    search_query = f"ytsearch{limit}:{query}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_query, download=False)

        for entry in result.get("entries", []):
            filesize = None
            if entry.get("formats"):
                best_audio = max(
                    (f for f in entry["formats"] if f.get("filesize")),
                    key=lambda f: f["filesize"],
                    default=None
                )
                if best_audio:
                    filesize = best_audio["filesize"]

        videos = []
        for entry in result.get("entries", []):
            videos.append(
                {
                    "title": entry.get("title", {}),
                    "id": entry.get('id'),
                    "duration_str": f"{entry.get('duration') // 60}:{entry.get('duration') % 60:02d}",
                    "filesize_mb": round(filesize / (1024 * 1024), 2) if filesize else None,
                }
            )
        return videos


def download_audio_from_youtube(query: str, output_path: str):
    yt_dlp_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'default_search': 'ytsearch1:',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with YoutubeDL(yt_dlp_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            title = info["entries"][0]["title"] if "entries" in info else info["title"]

        return output_path, title

    except Exception as e:
        logging.error(f"Error during YouTube download: {e}")
        return None


async def find_song_name_by_path(path: str):

    shazam = Shazam()
    try:
        out = await shazam.recognize(path)
        track = out.get("track", {})
        title = track.get("title", "")
        subtitle = track.get("subtitle", "")
        query = f"{title} {subtitle}".strip()

        if not query:
            logging.error("Shazam track info bo‘sh qaytdi")
            return None

        return query

    except Exception as e:
        logging.error(f"Shazam audio tanish xatolik: {e}", exc_info=True)
        return None





async def find_song_name_by_video(video_path: str):
    audio_path = f"./temp/{str(time.time_ns())}" + ".mp3"
    try:
        shazam = Shazam()
        ok = await asyncio.to_thread(extract_audio_from_video, video_path, audio_path)
        if not ok:
            return None
        out = await shazam.recognize(audio_path)
        track = out.get("track", {})
        title = track.get("title", "")
        subtitle = track.get("subtitle", "")
        query = f"{title} {subtitle}".strip()
        return query if query else None
    except Exception as e:
        print(f"Shazam xatolik: {e}")
        return None
    finally:
        if await asyncio.to_thread(os.path.exists, audio_path):
            await asyncio.to_thread(os.remove, audio_path)


async def handle_video(message: Message):
    video = message.video

    file = await message.bot.get_file(video.file_id)
    file_path = file.file_path
    download_path = f"./videos/{time.time_ns()}.mp4"

    await message.bot.download_file(file_path, download_path)

    song_name = await find_song_name_by_video(download_path)

    if await asyncio.to_thread(os.path.exists, download_path):
        await asyncio.to_thread(os.remove, download_path)

    if not song_name:
        return None

    return song_name


async def handle_voice(message: Message):
    if message.voice:
        audio = message.voice
    else:
        audio = message.audio
    file = await message.bot.get_file(audio.file_id)
    file_path = file.file_path
    download_path = f"./temp/{time.time_ns()}.mp3"

    await message.bot.download_file(file_path, download_path)

    song_name = await find_song_name_by_path(download_path)

    if not song_name:
        return None

    if await asyncio.to_thread(os.path.exists, download_path):
        await asyncio.to_thread(os.remove, download_path)

    return song_name
