import requests  # Импортируйте requests правильно
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

BACKEND_URL = "http://localhost:8000/course/api/"


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


from django.shortcuts import render, get_object_or_404
from django.conf import settings
import requests

def topics(request, pk):
    headers = {}

    token = request.session.get('token')  # Adjust based on your authentication setup
    if token:
        headers['Authorization'] = f'Token {token}'

    try:
        response_topics = requests.get(f"{BACKEND_URL}courses/{pk}/topics/", headers=headers)
        response_course = requests.get(f"{BACKEND_URL}courses/{pk}/", headers=headers)

        if response_topics.status_code == 200 and response_course.status_code == 200:
            topics = response_topics.json()
            course = response_course.json()
        else:
            topics = []
            course = None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for course {pk}: {e}")  
        topics = []
        course = None
    return render(request, "topics.html", {"topics": topics, "pk": pk, "course": course})

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
