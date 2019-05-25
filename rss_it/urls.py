"""rss_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from getter import views as getter_views
from gui import views as gui_views

urlpatterns = [
    # Gui
    path('', gui_views.Home, name='home'),

    # Feed Generators
    path('testfeed/', gui_views.TestFeed, name='test-feed'),
    path('search/<keyword>/', gui_views.Search, name='search'),
    path('channel/<channel_id>/', gui_views.ChannelIdFeed, name='channel-id-feed'),
    path('playlist/<playlist_id>/', gui_views.PlaylistIdFeed, name='playlist-id-feed'),
    # dumb but useful
    path('first/<keyword>/', gui_views.SearchFirstFeed, name='search-first-feed'),

    # Utility
    path('resize/<video_id>/', gui_views.Resize, name='resize'),

    # Gets the mp3 link from each video id
    path('get/<video_id>/', getter_views.Getter, name='getter'),

    # Admin
    path('admin/', admin.site.urls),
]
# 127.0.0.1:8000/get/FurdcPnisk0
