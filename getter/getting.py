from __future__ import unicode_literals
import youtube_dl

# App links to this, this gives a link to the mp3


def video_to_mp3(video_id):
    # Gets video id and returns mp3 (youtube-dl)
    ydl_opts = {
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)

    for form in info['formats']:
        # TODO make it so it prefers mp3 then m4a then aac then mp4?
        if form['ext'] in ['m4a', 'mp3', 'aac']:
            return form['url']

    print('error, could not find good audio file')
    return 'sorrydidntwork'

# video_to_mp3('-R6l_UERq_Q')