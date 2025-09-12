import time


def get_file_name() -> str:
    file_name = time.time_ns()
    return f"{file_name}.mp4"

def get_file_name_mp3() -> str:
    file_name = time.time_ns()
    return f"{file_name}"