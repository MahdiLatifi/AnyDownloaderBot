from yt_dlp import YoutubeDL


def download_video_pinterest(video_url):
    ydl_opts = {
        # 'format': 'best',
        'outtmpl': './downloads/%(title).80s.%(ext)s',
        'noplaylist': True,
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        # 'postprocessors': [],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Download error: {e}")


download_video_pinterest("https://pin.it/66oR7cSYv")



