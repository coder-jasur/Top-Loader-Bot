import asyncio
import os
import time

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from src.app.common.file.video import download_video
from src.app.keyboards.callback_data import MusicCD, VideoMusicCD
from src.app.keyboards.inline import video_keyboards, music_keyboards
from src.app.services.audio_download.shazam_function import (
    download_audio_from_youtube,
    handle_video, handle_voice, search_youtube, find_song_name_by_video
)
from src.app.services.video_download import get_info_for_size
from src.app.services.video_download.instagram import download_video_from_instagram
from src.app.services.video_download.tiktok import download_tiktok
from src.app.services.video_download.youtube import download_video_from_youtube
from src.app.texts import user_texts
from src.app.utils.downloader.all_downloader import AllDownloader

download_router = Router()


@download_router.message(F.text | F.video | F.voice | F.audio)
async def downloading(message: Message, lang: str):
    for f in [message.audio, message.voice, message.video]:
        if f:
            if f.file_size > 2 * 1024 * 1024 * 1024:
                await message.answer(user_texts["very_big_file"][lang])
                return

    load_msg = None
    video = None
    try:
        if message.text:
            if "https://" in message.text:
                load_msg = await message.reply(user_texts["video_is_loading"][lang])
                downloader = AllDownloader()
                if "tiktok.com" in message.text:
                    video_url, file_size = await download_tiktok(message.text)
                    if file_size:
                        if file_size > 2000:
                            await message.answer(user_texts["very_big_file"][lang])
                            return False
                    video = await download_video(video_url)
                    await message.answer_video(FSInputFile(video))
                    music = await find_song_name_by_video(video)
                    if music:
                        await message.reply_video(
                            FSInputFile(video),
                            reply_markup=video_keyboards(
                                music,
                                lang
                            ),
                            caption=user_texts["download_video"][lang]
                        )
                        await load_msg.delete()

                    else:
                        await message.reply_video(
                            FSInputFile(video),
                            caption=user_texts["download_video"][lang]
                        )

                    await asyncio.to_thread(os.remove, video)

                elif "instagram.com" in message.text:
                    video_path, music_name, instagram_downloader_errors = await (
                        downloader.insgtarm_video_music_downloader(
                            video_url=message.text
                        )
                    )

                    if music_name:
                        await message.reply_video(
                            FSInputFile(video_path),
                            reply_markup=video_keyboards(
                                music_name,
                                lang
                            ),
                            caption=user_texts["download_video"][lang]
                        )
                        await load_msg.delete()

                    else:
                        await message.reply_video(
                            FSInputFile(video_path),
                            caption=user_texts["download_video"][lang]
                        )

                    # info = await asyncio.to_thread(get_info_for_size, message.text)
                    # if info["filesize_mb"]:
                    #     if info["filesize_mb"] > 2000:
                    #         await message.answer(texts["very_big_file"][lang])
                    #         return False
                    #
                    #
                    # video = await asyncio.to_thread(download_video_from_instagram, message.text)
                    # music = await find_song_name_by_video(video)
                    #
                    # if music:
                    #     await message.reply_video(
                    #         FSInputFile(video),
                    #         reply_markup=video_keyboards(
                    #             music,
                    #             lang
                    #         ),
                    #         caption=texts["download_video"][lang]
                    #     )
                    #     await load_msg.delete()
                    #
                    # else:
                    #     await message.reply_video(
                    #         FSInputFile(video),
                    #         caption=texts["download_video"][lang]
                    #     )
                    #
                    # await asyncio.to_thread(os.remove, video)

                elif "youtube.com" in message.text:
                    info = await asyncio.to_thread(get_info_for_size, message.text)
                    if info["filesize_mb"] > 2000:
                        await message.answer(user_texts["very_big_file"][lang])
                        return False
                    video = await asyncio.to_thread(download_video_from_youtube, message.text)
                    music = await find_song_name_by_video(video)

                    if music:
                        await message.reply_video(
                            FSInputFile(video),
                            reply_markup=video_keyboards(
                                music,
                                lang
                            ),
                            caption=user_texts["download_video"][lang]
                        )
                        await load_msg.delete()

                    else:
                        await message.reply_video(
                            FSInputFile(video),
                            caption=user_texts["download_video"][lang]
                        )

                    await asyncio.to_thread(os.remove, video)
                else:
                    await load_msg.delete()
                    await message.answer(user_texts["wrong_link"][lang])
            else:
                load_msg = await message.answer(user_texts["music_is_loading"][lang])
                info = await asyncio.to_thread(search_youtube, message.text, 5)

                if not info:
                    await message.answer(user_texts["music_not_found"][lang])
                    await load_msg.delete()
                i = 0
                while i < len(info):
                    filesize = info[i].get("filesize_mb")
                    duration = info[i].get("duration_str")

                    if filesize is None or duration is None:
                        i += 1
                        continue

                    if int(filesize) > 2000 or int(duration[0]) > 10:
                        await message.answer(user_texts["music_not_found"][lang])
                        await load_msg.delete()
                        return

                    i += 1

                text = ""
                for i, video in enumerate(info, start=1):
                    text += f"{i}. {video['title']} - {video['duration_str']}\n"

                await message.answer(text=text, reply_markup=music_keyboards(info))
                await load_msg.delete()

        elif message.video:
            load_msg = await message.answer(user_texts["music_is_loading"][lang])
            music = await handle_video(message)
            if music:
                info = await asyncio.to_thread(search_youtube, music, 5)

                if not info:

                    await message.answer(user_texts["music_not_found"][lang])
                    await load_msg.delete()
                    return
                i = 0

                while i < len(info):
                    filesize = info[i].get("filesize_mb")
                    duration = info[i].get("duration_str")

                    if filesize is None or duration is None:
                        i += 1
                        continue

                    if int(filesize) > 2000 or int(duration[0]) > 10:
                        await message.answer(user_texts["music_not_found"][lang])
                        await load_msg.delete()
                        return

                    i += 1

                text = ""
                for i, video in enumerate(info, start=1):
                    text += f"{i}. {video['title']} - {video['duration_str']}\n"

                await message.answer(text=text, reply_markup=music_keyboards(info))
                await load_msg.delete()
                return

            await message.answer(user_texts["music_not_found"][lang])
            await load_msg.delete()

        elif message.audio or message.voice:
            load_msg = await message.answer(user_texts["music_is_loading"][lang])

            music_name = await handle_voice(message)

            if music_name:
                info = await asyncio.to_thread(search_youtube, music_name, 5)

                if not info:
                    await message.answer(user_texts["music_not_found"][lang])
                    await load_msg.delete()
                i = 0
                while i < len(info):
                    filesize = info[i].get("filesize_mb")
                    duration = info[i].get("duration_str")

                    if filesize is None or duration is None:
                        i += 1
                        continue

                    if int(filesize) > 2000 or int(duration[0]) > 10:
                        await message.answer(user_texts["music_not_found"][lang])
                        await load_msg.delete()
                        return

                    i += 1

                text = ""
                for i, video in enumerate(info, start=1):
                    text += f"{i}. {video['title']} - {video['duration_str']}\n"

                await message.answer(text=text, reply_markup=music_keyboards(info))
                await load_msg.delete()
                return

            await message.answer(user_texts["music_not_found"][lang])
            await load_msg.delete()


    except Exception as e:
        print(e)
        await message.answer(text=user_texts["error_in_loading"][lang])
    finally:
        if load_msg:
            await load_msg.delete()

        if video:
            if await asyncio.to_thread(os.path.exists, video):
                await asyncio.to_thread(os.remove, video)


@download_router.callback_query(MusicCD.filter())
async def get_tiktok_video_mp3(call: CallbackQuery, callback_data: MusicCD, lang: str):
    load_msg = await call.message.answer(user_texts["music_is_loading"][lang])
    audio_path = f"temp/{time.time_ns()}.mp3"
    downloaded_file = None
    try:
        downloaded_file, title = await asyncio.to_thread(
            download_audio_from_youtube,
            f"https://www.youtube.com/watch?v={callback_data.music_name}",
            audio_path
        )
        await call.message.reply_audio(
            FSInputFile(f"{downloaded_file}.mp3"),
            caption=user_texts["download_video"][lang],
            title=title
        )
    except Exception as e:
        print(e)
        await call.message.answer(text=user_texts["error_in_loading_music"][lang])
    finally:
        if load_msg:
            await load_msg.delete()
        if os.path.exists(f"{downloaded_file}.mp3"):
            await asyncio.to_thread(os.remove, f"{downloaded_file}.mp3")


@download_router.callback_query(VideoMusicCD.filter())
async def get_tiktok_video_mp3(call: CallbackQuery, callback_data: VideoMusicCD, lang: str):
    load_msg = await call.message.answer(user_texts["music_is_loading"][lang])
    info = await asyncio.to_thread(search_youtube, callback_data.music_name, 5)

    if not info:
        await call.message.answer(user_texts["music_not_found"][lang])
        await load_msg.delete()
    i = 0
    while i < len(info):
        filesize = info[i].get("filesize_mb")
        duration = info[i].get("duration_str")

        if filesize is None or duration is None:
            i += 1
            continue

        if int(filesize) > 2000 or int(duration[0]) > 10:
            await call.message.answer(user_texts["music_not_found"][lang])
            await load_msg.delete()
            return

        i += 1

    text = ""
    for i, video in enumerate(info, start=1):
        text += f"{i}. {video['title']} - {video['duration_str']}\n"

    await call.message.answer(text=text, reply_markup=music_keyboards(info))
    await load_msg.delete()


@download_router.callback_query(F.data == "delete_list_music")
async def delite_music_menu(call: CallbackQuery):
    await call.message.delete()
