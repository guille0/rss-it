# Youtube channel to rss feed
# Twitch channel to rss feed? (Recorded videos)

# Youtube API Key: 'AIzaSyCkIU2qa_ZmuvUJxH-B8nIlQyewthIvFT0'

from __future__ import unicode_literals
import youtube_dl

# App links to this, this gives a link to the mp3


def video_to_mp3(video_id):
    # Gets video id and returns mp3 (youtube-dl)
    
    ydl_opts = {
        'quiet': True,
        'format': 'm4a'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)
        # ydl.download([video_id])
        # print(info)
    
    print(info)
    return 'hey'
    return info['formats'][0]['url'], info['formats'][0]['filesize']
print('hey')
print(video_to_mp3('KOSrUDjkTW0'))