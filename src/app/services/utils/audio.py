import os
import subprocess


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
        print("ERROR", e)
        return False