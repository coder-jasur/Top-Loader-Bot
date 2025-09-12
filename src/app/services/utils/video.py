import aiofiles
from aiogram.client.session import aiohttp

from src.app.services.utils.files import get_file_name


async def download_video(url: str, file_name: str) -> str | None:
    save_path = f"./media/videos/{file_name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    await f.write(await response.read())
                return save_path