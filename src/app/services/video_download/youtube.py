from yt_dlp import YoutubeDL

from src.app.common.file.video import gen_video_file_name


def download_video_from_youtube(video_url: str) -> str:
    output_file_name = gen_video_file_name()
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
