import time

import aiofiles
import aiohttp


def gen_video_file_name() -> str:
    file_name = time.time_ns()
    return f"{file_name}.mp4"


async def download_video(url: str) -> str | None:
    file_name = gen_video_file_name()
    save_path = f"./videos/{file_name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    await f.write(await response.read())
                return save_path