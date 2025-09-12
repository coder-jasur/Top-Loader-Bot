import time

from yt_dlp import YoutubeDL


def download_video_from_instagram(video_url: str) -> str:
    output_file_name = f"{time.time_ns()}.mp4"
    output_path = f"./videos/{output_file_name}"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return output_path
