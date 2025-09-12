import aiohttp


async def download_tiktok(url):
    api_url = f"https://tiktok-dl.akalankanime11.workers.dev/?url={url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            if resp.status != 200:
                print(f"❌ API xato: {resp.status}")
                return
            data = await resp.json()

    no_wm = data.get("non_watermarked_url")
    file_size = data.get("file_size")
    file_size = round(file_size / (1024 * 1024), 2)
    if not no_wm:
        print("❌ Video URL topilmadi")
        return
    return no_wm, file_size










