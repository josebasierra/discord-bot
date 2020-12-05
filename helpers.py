from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

def get_audio(url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    return FFmpegPCMAudio(URL, executable=r"C:\Users\joseb\Desktop\Programs\discord_bot\ffmpeg\bin\ffmpeg.exe", **FFMPEG_OPTIONS)

