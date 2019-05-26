from __future__ import unicode_literals
import youtube_dl

# Rss feed links every episode to this, this redirects to the audio file


def video_to_mp3(video_id):
    # Gets video id and returns mp3 (youtube-dl)

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)

    for form in info['formats']:
        if form['ext'] == 'm4a':
            return form['url']

    for form in info['formats']:
        if form['ext'] == 'mp3':
            return form['url']

    print(f'Could not find mp3/m4a audio file for {video_id}, sending webm')
    return info['formats'][0]['url']
