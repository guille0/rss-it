from __future__ import unicode_literals
from feedgen.feed import FeedGenerator
# sudo pip3 install feedgen
import youtube_dl


def video_to_mp3(video_id):
    # Gets video id and returns mp3 (youtube-dl)
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)
        # print(info)
    return info['formats'][0]['url'], info['formats'][0]['filesize']

# video_to_mp3('-R6l_UERq_Q')


class Rss:
    def __init__(self, title='', link='', logo='', description='none'):
        self.title = title
        self.fg = FeedGenerator()
        self.fg.load_extension('podcast')
        self.fg.title(title)
        self.fg.description(description)
        self.fg.link(href=link, rel='alternate')

        # Logo is squashed (should be square)
        # Link to a page that returns a squared thumbnail? with top and bottom lines
        if logo:
            self.fg.logo(logo)

    def add_video(self, video_id, title, pubdate, description=''):
        fe = self.fg.add_entry()
        link, length = video_to_mp3(video_id)
        fe.id(link)
        fe.title(title)
        # Get the first paragraph of the description?
        fe.description(description)
        fe.pubDate(pubdate)
        fe.enclosure(url=link, length=length type='audio/mpeg')

    def export(self):
        return self.fg.rss_str(pretty=True)
