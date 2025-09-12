import os
import subprocess

from src.app.common.file.video import gen_video_file_name


import aiohttp
import aiofiles

async def download_audio(url: str) -> str | None:
    file_name = gen_video_file_name()
    save_path = f"./temp/{file_name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    await f.write(await response.read())
                return save_path



def extract_audio_from_video(video_path: str, audio_path: str) -> bool:
    try:
        cmd = [
            "ffmpeg", "-y", "-i", video_path,
            "-vn",
            "-acodec", "mp3",
            audio_path
        ]
        subprocess.run(cmd)
        return os.path.exists(audio_path)
    except Exception as e:
        print(f"FFmpeg xatolik: {e}")
        return False