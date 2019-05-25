from __future__ import unicode_literals
import youtube_dl

# App links to this, this gives a link to the mp3


def video_to_mp3(video_id):
    # Gets video id and returns mp3 (youtube-dl)
    ydl_opts = {
        'quiet': True,
        'format': 'm4a',
        # Try also 'aac'
        # 'prefer_ffmpeg': True,
        # 'ext': 'mp3'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)
        print(info['formats'][0]['ext'])
        # print(info)
    return info['formats'][0]['url']

# video_to_mp3('-R6l_UERq_Q')