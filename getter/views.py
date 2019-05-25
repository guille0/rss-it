from django.shortcuts import render, redirect, reverse
from django.http import request, HttpResponseRedirect
from . import getting


def Getter(request, video_id):
    # test example: http://127.0.0.1:8000/get/FurdcPnisk0/

    guy = getting.video_to_mp3(video_id)

    return HttpResponseRedirect(guy)
