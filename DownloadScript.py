# 1-instagram🔴
# 2-youtube🟢
# 3-pintrest🟢
# 4-tiktok🟢
# 5-linkedin🟢
# 6-soundcloud🟢
# 7-spotify🔴

from yt_dlp import YoutubeDL
from random import choices
from string import ascii_letters, digits

def random_string(length=18):
    return ''.join(choices(ascii_letters + digits, k=length))


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

