import requests  # Импортируйте requests правильно
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

BACKEND_URL = "http://127.0.0.1:8000/course/api/"


def courses(request):
    try:
        response = requests.get(
            f"{BACKEND_URL}courses/"
        )
        if response.status_code == 200:
            courses = response.json()
        else:
            courses = []
    except requests.exceptions.RequestException as e:
        courses = []  # Если ошибка, возвращаем пустой список

    return render(request, "courses.html", {"course_list": courses})


def topics(request, pk):
    try:
        response = requests.get(f"{BACKEND_URL}courses/{pk}/topics/")
        if response.status_code == 200:
            topics = response.json()
        else:
            topics = []
    except requests.exceptions.RequestException as e:
        topics = []

    return render(request, "topics.html", {"topics": topics, "pk": pk})


# def videos(request, pk, topic_id):
#     try:
#         response = requests.get(f'{BACKEND_URL}courses/{pk}/topics/{topic_id}/videos')
#         if response.status_code == 200:
#             videos = response.json()
#         else:
#             videos = []
#     except requests.exceptions.RequestException as e:
#         videos = []
#
#     return render(request, 'videos.html', {'videos': videos})
