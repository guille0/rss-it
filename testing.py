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
        'format': 'bestaudio/best',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)

    print(info['formats'])

    for form in info['formats']:
        if form['ext'] == 'mp3':
            print(form['ext'], form['url'])
            return form['url']
    
    for form in info['formats']:
        if form['ext'] == 'm4a':
            print(form['ext'], form['url'])
            return form['url']

    print('error, could not find good audio file')
    return 'sorrydidntwork'
# print("http://traffic.libsyn.com/anjunabeats/ABGT326_LiveShow1204198377.m4a".endswith('.mp3'))
print(video_to_mp3('eWiPEDGovNk'))