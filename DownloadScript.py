# 1-instagram🔴
# 2-youtube🟢
# 3-pintrest🟢
# 4-tiktok🟢
# 5-linkedin🟢
# 6-soundcloud🟢
# 7-spotify🔴

from instagrapi import Client as InstaClient
from instagrapi.exceptions import LoginRequired
import InstaConfigs
from yt_dlp import YoutubeDL
from random import choices
from string import ascii_letters, digits
import os
import logging


# =================================================================== Configs ===================================================================
# ===============================================================================================================================================

cl = InstaClient()
cl.login(InstaConfigs.ACCOUNT_USERNAME, InstaConfigs.ACCOUNT_PASSWORD)
cl.set_settings(InstaConfigs.THE_SETTINGS)
# cl.dump_settings("InstaSession.json")
os.makedirs("./downloads", exist_ok=True)


logger = logging.getLogger()


def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    session = cl.load_settings("InstaSession.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(InstaConfigs.ACCOUNT_USERNAME, InstaConfigs.ACCOUNT_PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info(
                    "Session is invalid, need to login via username and password"
                )

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(InstaConfigs.ACCOUNT_USERNAME, InstaConfigs.ACCOUNT_PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info(
                "Attempting to login via username and password. username: %s"
                % InstaConfigs.ACCOUNT_USERNAME
            )
            if cl.login(InstaConfigs.ACCOUNT_USERNAME, InstaConfigs.ACCOUNT_PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")


def random_string(length=18):
    return ''.join(choices(ascii_letters + digits, k=length))

# =================================================================== Instagram ===================================================================
# =================================================================================================================================================

def download_insta_post_by_url(url):
    pk = cl.media_pk_from_url(url)
    media = cl.media_info(pk)
    
    the_folder = random_string()
    os.makedirs(f"downloads/{the_folder}", exist_ok=True)
    if media.media_type == 1:  # Photo
        cl.photo_download(pk, folder=f"downloads/{the_folder}")
        return f"downloads/{the_folder}"
    elif media.media_type == 2:  # Video
        cl.video_download(pk, folder=f"downloads/{the_folder}")
        return f"downloads/{the_folder}"
    elif media.media_type == 8:  # Album
        cl.album_download(pk, folder=f"downloads/{the_folder}")
        return f"downloads/{the_folder}"
    else:
        raise Exception("Unsupported media type")


def story_downloader_by_url(url):
    file_name = cl.story_download(
        story_pk=cl.story_pk_from_url(url), folder="downloads"
    )
    return file_name


def story_downloader_by_username(username):
    stories_of_user = cl.user_stories(cl.user_id_from_username(username))
    os.makedirs(f"downloads/{username}", exist_ok=True)
    for story in stories_of_user:
        cl.story_download(story_pk=story.pk, folder=f"downloads/{username}")
    return f"./downloads/{username}"


# =================================================================== ALL ===================================================================
# ===========================================================================================================================================

def download_video_pinterest_tiktok_reel_linkedin(video_url):
    ydl_opts = {
        'outtmpl': f'./downloads/%{random_string()}.%(ext)s',
        'noplaylist': True,
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            return ydl.prepare_filename(info), info
    except Exception as e:
        print(f"Download error: {e}")

# =================================================================== Youtube ===================================================================
# ===============================================================================================================================================

def list_resolutions_youtube(video_url):
    ydl_opts = {
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get('formats', [])

        resolutions = []
        for fmt in formats:
            if fmt.get('vcodec') != 'none':
                if "vp09" in fmt.get('vcodec'):
                    resolution = fmt.get('format_note') or fmt.get('height')
                    resolutions.append({
                        'resolution': resolution,
                        'fps': fmt.get('fps'),
                        'format_id': fmt['format_id'],
                    })

        return resolutions


def download_youtube_with_resolotion(video_url, resolotion):
    ydl_opts = {
        'format': f"{resolotion}+bestaudio",
        'merge_output_format': 'mp4',
        'outtmpl': f'./downloads/{random_string()}.%(ext)s',
        'noplaylist': True,
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'cookiefile': "yt_cookies.txt",
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            return ydl.prepare_filename(info), info
    except Exception as e:
        print(f"Download error: {e}")


# =================================================================== SoundCloud ===================================================================
# ==================================================================================================================================================

def download_tack_soundcloud(url, output_folder="tracks"):
    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "audio-quality": "best",
        "noplaylist": True,
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegMetadata",
            },
            {
                "key": "EmbedThumbnail",
            },
        ],
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "addmetadata": True,
        'quiet': True,
        'no_warnings': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        thumb = ""
        for form in info["thumbnails"]:
            if form["id"] == "t300x300":
                t = form["url"]
                print(t)
        return ydl.prepare_filename(info), thumb


def download_playlist_soundcoud(url):
    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "audio-quality": "best",
        "writethumbnail": True,
        "noplaylist": False,
        "postprocessors": [
            {
                "key": "FFmpegMetadata",
            },
            {
                "key": "EmbedThumbnail",
            },
        ],
        "outtmpl": "tracks/%(playlist_title)s/%(title)s.%(ext)s",
        "addmetadata": True,
        'quiet': True,
        'no_warnings': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"./tracks/{info['album']}"


# login_user()
p = download_insta_post_by_url("https://www.instagram.com/reel/DKFOXpRNk68/?utm_source=ig_web_copy_link")
print(p)