from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .youtube import FeedCreator, channel_to_playlist
from skimage import io as skio
from PIL import Image
import io


def Home(request):
    if request.method == 'POST':
        # do all things
        input_value = request.POST.get('value').replace('/', '')
        # input_type = request.POST.get('type')

        # return redirect(input_type, input_value)
        return redirect('search', input_value)

    return render(request, 'gui/home.html')


def Resize(request, video_id):
    # img = io.imread('https://i.stack.imgur.com/DNM65.png')[:, :, :-1]
    # Download image in bytes, add ¿black? bars, serve it
    # https://i.ytimg.com/vi/QhR2VGia0-s/mqdefault.jpg

    # Test: 
    url = 'https://i.ytimg.com/vi/' + video_id + '/mqdefault.jpg'

    baseimg = skio.imread(url)

    end = Image.fromarray(baseimg)

    old_size = end.size

    new_size = (max(old_size), max(old_size))
    new_im = Image.new("RGB", new_size)
    new_im.paste(end, ((new_size[0]-old_size[0])//2,
                       (new_size[1]-old_size[1])//2))

    imgByteArr = io.BytesIO()
    new_im.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()

    return HttpResponse(imgByteArr, content_type='image')


def Search(request, keyword):
    # Looks for channels with keyword
    # Test: 127.0.0.1:8000/search/zfg

    guy = FeedCreator(request)
    results = guy.search(keyword, 10)

    # This redirects you to the rss feed if there's only 1 result in the search
    # if len(results) == 1:
    #     if results[0].kind == 'youtube#channel':
    #         return redirect('channel-id-feed', results[0].id)

    #     if results[0].kind == 'youtube#playlist':
    #         return redirect('playlist-id-feed', results[0].id)

    # Test
    # results = [{'kind':'youtube#playlist',
    #             'title': 'Zfg highlights!',
    #             'smallthumbnail': 'https://i.ytimg.com/vi/QhR2VGia0-s/default.jpg',
    #             'channel': 'zfg',
    #             'id': '2312'}]

    root = 'http://' + request.get_host()

    # channel.title, id, description, thumbnail
    return render(request, 'gui/channel-search.html', context={'results': results, 'root': root})


def ChannelIdFeed(request, channel_id):
    # Creates a feed out of the given channel id
    # Test: 127.0.0.1:8000/channel/UCk9RA3G-aVQXvp7-Q4Ac9kQ
    guy = FeedCreator(request)
    feed = guy.channel_id(channel_id, 200)

    if feed is None:
        return HttpResponse('Channel not found.')

    return HttpResponse(feed, content_type='text/xml')


def PlaylistIdFeed(request, playlist_id):
    # Creates a feed out of the given playlist id
    # Test: 127.0.0.1:8000/playlist/PL3XZNMGhpynMm0Ywj-rupAKwRryWzEQy-
    guy = FeedCreator(request)
    feed = guy.playlist_id(playlist_id, 200)

    if feed is None:
        return HttpResponse('Playlist not found.')

    return HttpResponse(feed, content_type='text/xml')


def SearchFirstFeed(request, keyword):
    # Just for messing around

    # Creates a feed out of the first result in a search (so be accurate)
    # Test: 127.0.0.1:8000/channelfirst/zfg
    guy = FeedCreator(request)
    feed = guy.search_first_result(keyword, 200)

    return HttpResponse(feed, content_type='text/xml')


def TestFeed(request):
    # Creates a test feed
    guy = FeedCreator(request)
    feed = guy.playlist_id('PL3XZNMGhpynMm0Ywj-rupAKwRryWzEQy-', 10)

    return HttpResponse(feed, content_type='text/xml')
