import requests
from django.shortcuts import render

BACKEND_URL = "http://142.93.171.201:8000/video/api/"


def video_list(request, topic_id, pk):
    try:
        response = requests.get(f"{BACKEND_URL}videos/{topic_id}")
        if response.status_code == 200:
            videos = response.json()
        else:
            videos = []
    except requests.exceptions.RequestException as e:
        videos = []

    return render(
        request, "videos.html", {"video_list": videos, "pk": pk, "topic_id": topic_id}
    )


def video_detail(request, video_id, pk, topic_id):
    response = requests.get(f"{BACKEND_URL}video/{video_id}/")
    video = response.json()
    return render(request, "video.html", {"video": video})
