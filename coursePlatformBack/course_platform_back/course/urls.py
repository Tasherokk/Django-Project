# urls.py
from django.urls import path
from .views import get_courses, get_topics, get_videos

urlpatterns = [
    path('api/courses/', get_courses, name='get_courses'),
    path('api/courses/<int:course_id>/topics/', get_topics, name='get_topics'),
    path('api/courses/<int:course_id>/topics/<int:topic_id>/videos', get_videos, name='get_videos'),

]
