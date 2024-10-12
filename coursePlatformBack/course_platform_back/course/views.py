# views.py
from django.http import JsonResponse
from .models import Course, Topic  # Предположим, у вас есть модели Course и Topic
from video.models import Video


def get_courses(request):
    courses = Course.objects.all()
    course_data = [{"id": course.id, "title": course.title, "description": course.description, "created_at": course.created_at} for course in courses]
    return JsonResponse(course_data, safe=False)

def get_topics(request, course_id):
    topics = Topic.objects.filter(course_id=course_id)
    topic_data = [{"id": topic.id, "title": topic.title, "description": topic.description} for topic in topics]
    return JsonResponse(topic_data, safe=False)


def get_videos(request, topic_id):
    videos = Video.objects.filter(topic_id=topic_id).values('id', 'title', 'description', 'image', 'create_at')
    return JsonResponse(list(videos), safe=False)