import random
import string
import time

import subprocess
from instagrapi import Client as c
from instagrapi.exceptions import LoginRequired

import asyncio
from concurrent.futures import ThreadPoolExecutor

# import jdatetime
import requests
import os
from InstaConfigs import *
from random import choices
from string import ascii_letters, digits

executor = ThreadPoolExecutor()


def random_string(length=18):
    return "".join(choices(ascii_letters + digits, k=length))


def download_story_link(url):
    cl = c()
    try:
        cl.load_settings("InstaSession.json")
        print("seesionnn")
    except FileNotFoundError:
        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
        cl.dump_settings("InstaSession.json")
    media_pk = cl.story_pk_from_url(url)
    x = cl.story_download(media_pk, "./downloads")
    print(x)
    return x


async def download_story(url):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, download_story_link, url)


def download_reel_link(url):
    cl = c()
    try:
        cl.load_settings("InstaSession.json")
    except FileNotFoundError:
        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
        cl.dump_settings("InstaSession.json")
    media_pk = cl.media_pk_from_url(url)
    try:
        x = cl.album_download(int(media_pk), "./downloads")
    except:
        try:
            x = cl.photo_download(int(media_pk), "./downloads")
        except:
            x = cl.clip_download(int(media_pk), "./downloads")
    print(x)
    y = cl.media_info(media_pk)
    try:
        list_info = [
            y.like_count,
            y.play_count,
            y.comment_count,
            y.caption_text,
            y.user.username,
        ]
    except:
        try:
            list_info = [
                y.like_count,
                y.view_count,
                y.comment_count,
                y.caption_text,
                y.user.username,
            ]
        except:
            list_info = [y.like_count, y.view_count, y.comment_count, y.caption_text]
    # print(list_info)
    return x, list_info


def download_instagram_profile_pic(username_profile, save_path=None):
    try:
        cl = c()
        try:
            cl.load_settings("InstaSession.json")
        except FileNotFoundError:
            cl.login(ACCOUNT_PASSWORD, ACCOUNT_PASSWORD)
            cl.dump_settings("InstaSession.json")
        print(username_profile)
        user = cl.user_info_by_username(username_profile)
        print("ok")
        profile_pic_url = user.profile_pic_url_hd
        response = requests.get(str(profile_pic_url))
        response.raise_for_status()

        filename = f"{username_profile}_profile_pic.jpg"
        if save_path:
            filename = os.path.join(save_path, filename)

        # ذخیره تصویر
        with open(filename, "wb") as f:
            f.write(response.content)
        if user.is_private:
            list_info = [
                user.full_name,
                user.follower_count,
                user.following_count,
                user.media_count,
                user.biography,
                "بسته (پرایوت) 🔓",
            ]
        else:
            list_info = [
                user.full_name,
                user.follower_count,
                user.following_count,
                user.media_count,
                user.biography,
                "باز (پابلیک) 🔓",
            ]
        return filename, list_info

    except Exception as e:
        print(e)
        return None


async def download_reel(url):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, download_reel_link, url)


# def get_date_now():
#     now = jdatetime.datetime.now() + jdatetime.timedelta(hours=3, minutes=30)
#     formatted_date = now.strftime("%Y/%m/%d, %H:%M:%S")

#     return formatted_date


def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits
    random_code = "".join(random.choice(characters) for _ in range(length))
    return random_code


def extract_audio_with_ffmpeg(video_path, output_audio_path="output_audio.mp3"):
    command = [
        "ffmpeg",
        "-i",
        video_path,  # مسیر ویدیوی ورودی
        "-vn",  # بدون ویدیو
        "-acodec",
        "libmp3lame",  # کدک MP3
        "-q:a",
        "2",  # کیفیت صدا
        output_audio_path,  # مسیر خروجی صدا
    ]

    try:
        subprocess.run(command, check=True)
        return output_audio_path
    except subprocess.CalledProcessError as e:
        return False
