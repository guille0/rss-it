from __future__ import unicode_literals
from feedgen.feed import FeedGenerator
# sudo pip3 install feedgen


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

    def add_video(self, link, title, pubdate, description=''):
        fe = self.fg.add_entry()
        fe.id(link)
        fe.title(title)
        # Get the first paragraph of the description?
        fe.description(description)
        fe.pubDate(pubdate)

        mimetype = 'audio/mpeg'
        if link.endswith('.m4a'):
            mimetype = 'audio/mp4'
        elif link.endswith('.mp3'):
            mimetype = 'audio/mpeg'
        # add more formats if needed (usually works with audio/mpeg by default)

        fe.enclosure(link, '0', mimetype)

    def export(self):
        return self.fg.rss_str(pretty=True)
