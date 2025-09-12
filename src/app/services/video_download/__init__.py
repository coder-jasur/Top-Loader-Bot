from typing import Any

from yt_dlp import YoutubeDL


def get_info_for_size(video_url: str):

    with YoutubeDL({}) as ydl:
        info = ydl.extract_info(video_url, download=False)

        if "entries" in info:
            info = info["entries"][0]

        duration = info.get("duration")
        filesize = info.get("filesize") or info.get("filesize_approx")

        return {
            "duration_sec": duration,
            "duration_min": round(duration / 60, 2) if duration else None,
            "filesize_mb": round(filesize / (1024 * 1024), 2) if filesize else None,
        }


