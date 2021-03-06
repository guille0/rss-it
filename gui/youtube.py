import googleapiclient.discovery
import googleapiclient.errors
from .helpers import Singleton, time_to_pubdate, parse_time
from .rss import Rss
from django.shortcuts import reverse
import os


def video_url(root, url):
    rest = reverse('getter', kwargs={'video_id': url})

    return root + rest


def channel_to_playlist(channel_id):
    # returns playlist, title, thumbnail
    api = YoutubeAPI.instance()

    request = api.youtube.channels().list(
        fields='items(snippet(title,thumbnails(medium(url))),contentDetails(relatedPlaylists(uploads)))',
        part='contentDetails,snippet',
        id=channel_id,
    )
    response = request.execute()
    playlist = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    title = response['items'][0]['snippet']['title']
    thumbnail = response['items'][0]['snippet']['thumbnails']['medium']['url']

    if len(response['items']) > 0:
        return playlist, title, thumbnail
    else:
        return None, None, None


def get_playlist(playlist_id, max_results=100):
    'max_results=-1 gets all the videos in the playlist'
    # Set a result limit so we don't blow the quota with huge channels/playlists
    api = YoutubeAPI.instance()

    data = {}

    # Get playlist metadata
    request = api.youtube.playlists().list(
        fields='items(snippet(title,description,thumbnails(medium(url)),channelTitle))',
        part='snippet,contentDetails',
        id=playlist_id,
        )
    response = request.execute()

    if len(response['items']) == 0:
        return None

    response = response['items'][0]

    data['title'] = response['snippet']['title']
    data['description'] = response['snippet']['description'] or data['title']
    # data['thumbnail'] = response['snippet']['thumbnails']['medium']['url']
    data['channel'] = response['snippet']['channelTitle']
    data['link'] = 'https://www.youtube.com/playlist?list=' + playlist_id

    # max_results = -1  means get all the videos in the playlist
    if max_results == -1:
        max_results = response['contentDetails']['itemCount']

    # Get videos
    todo = max_results
    nextpage = ''
    data['items'] = []

    while todo > 0:
        results_per_query = todo if todo <= 50 else 50

        request = api.youtube.playlistItems().list(
            fields='nextPageToken,items(snippet(title,position,resourceId,publishedAt,description))',
            part='snippet',
            playlistId=playlist_id,
            maxResults=results_per_query,
            pageToken=nextpage
        )
        response = request.execute()

        data['items'] += response['items']
        try:
            # If there's a next page, go to it
            nextpage = response['nextPageToken']
            todo -= results_per_query

        except KeyError:
            # If there isn't, finish up
            todo = 0

    return data


def clean_description(description):
    description = ''.join(description).lstrip()

    # Gets first paragraph of the description
    # description = description.split('\n')[0]
    return description


@Singleton
class YoutubeAPI:

    def __init__(self):
        # Change to actual key for DEBUG ging
        self.key = os.environ.get('YOUTUBE_API_KEY')

        api_service_name = 'youtube'
        api_version = 'v3'
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=self.key)

    def search(self, keyword, max_results):

        request = self.youtube.search().list(
            safeSearch='none',
            fields='items(id,snippet(title,description,thumbnails(medium(url),default(url)),channelTitle))',
            part='snippet',
            maxResults=max_results,
            type='channel,playlist',
            q=keyword,
        )
        response = request.execute()

        results = [SearchResult(guy) for guy in response['items']]

        return results


class SearchResult:
    def __init__(self, data):
        self.kind = data['id']['kind']
        if self.kind == 'youtube#channel':
            self.id = data['id']['channelId']
        if self.kind == 'youtube#playlist':
            self.id = data['id']['playlistId']

        self.title = data['snippet']['title']
        self.channel = data['snippet']['channelTitle']
        self.description = data['snippet']['description']
        self.smallthumbnail = data['snippet']['thumbnails']['default']['url']
        self.thumbnail = data['snippet']['thumbnails']['medium']['url']
        self.api = YoutubeAPI.instance()

    def __repr__(self):
        return f'{self.title}'

    def playlist(self):
        'Returns the "channel uploads" playlist id of a channel'
        if self.kind == 'youtube#channel':
            return self.kind, channel_to_playlist(self.id)
        if self.kind == 'youtube#playlist':
            return self.kind, self.id


class Playlist:
    def __init__(self, playlist_id, root, max_results=100, title=None, thumbnail=None):
        data = get_playlist(playlist_id, max_results)

        self.root = root
        self.valid = False

        if data is None:
            self.valid = False
        else:
            items = data['items']

            if len(items) > 0:
                self.valid = True

                self.videos = [Video(guy) for guy in items]
                self.channel = data['channel']
                self.description = data['description']
                self.link = data['link']

                if thumbnail is None:
                    self.thumbnail = self.root+reverse('resize', kwargs={'video_id': self.videos[0].id})
                else:
                    self.thumbnail = thumbnail

                if title is None:
                    self.title = data['title']
                else:
                    self.title = title

    def __getitem__(self, i):
        return self.videos[i]

    def __len__(self):
        return len(self.videos)

    def __repr__(self):
        return (f'Title: {self.title}\n'
                f'by: {self.channel}\n'
                f'thumbnails: {self.thumbnail}')

    def sort_by_date(self):
        # Sorts videos by date added
        self.videos.sort(key=lambda x: x.date)

    def sort_by_playlist_order(self):
        # Sorts videos by normal playlist order
        self.videos.sort(key=lambda x: x.position)

    def to_rss(self):
        feed = Rss(title=self.title, link=self.link,
                   logo=self.thumbnail, description=self.description)

        for video in self.videos:
            feed.add_video(link=video_url(self.root, video.id), title=video.title,
                           pubdate=time_to_pubdate(video.date), description=video.description)

        return feed.export()


class Video:
    def __init__(self, data):
        # snippet(title,position,resourceId,publishedAt)
        resource_id = data['snippet']['resourceId']
        if resource_id['kind'] == 'youtube#video':
            self.id = resource_id['videoId']
        else:
            self.id = None

        self.title = data['snippet']['title']
        self.position = data['snippet']['position']
        self.date = parse_time(data['snippet']['publishedAt'])
        description = data['snippet']['description']
        self.description = clean_description(description)

    def __repr__(self):
        return (f'Title: {self.title}\n'
                f'Position: {self.position}\n'
                f'Video id: {self.id}\n'
                f'Date: {self.date}')


class FeedCreator:
    def __init__(self, request):
        self.request = request

        self.root = 'http://' + self.request.get_host()

    def search(self, keyword, max_results):
        'Returns a "max_results" number of search results'

        youtube = YoutubeAPI.instance()
        results = youtube.search(keyword, max_results)

        return results

    def playlist_id(self, playlist_id, max_results):
        # Turns playlist into a feed
        playlist = Playlist(playlist_id, root=self.root, max_results=max_results)

        if playlist.valid is False:
            return None
        # playlist.sort_by_playlist_order()

        rss = playlist.to_rss()

        return rss

    def channel_id(self, channel_id, max_results):
        # Turns channel into a feed
        playlist_id, title, thumbnail = channel_to_playlist(channel_id)

        if playlist_id is None:
            return None

        playlist = Playlist(playlist_id, root=self.root, max_results=max_results,
                            title=title, thumbnail=thumbnail)

        # Channels are always sorted by date
        playlist.sort_by_date()

        rss = playlist.to_rss()

        return rss

# Dumb stuff
    def search_first_result(self, keyword, max_results):
        'Creates a feed out of the first channel or playlist it finds'
        youtube = YoutubeAPI.instance()
        results = youtube.search(keyword, 1)

        if len(results) < 1:
            return None

        # Gets the first channel or playlist
        kind, plist = results[0].playlist()

        if kind == 'youtube#channel':
            playlist = Playlist(plist[0], root=self.root, max_results=max_results,
                                title=plist[1], thumbnail=plist[2])
        if kind == 'youtube#playlist':
            playlist = Playlist(plist, root=self.root, max_results=max_results)

        if playlist.valid is False:
            return None

        playlist.sort_by_date()

        rss = playlist.to_rss()

        return rss
