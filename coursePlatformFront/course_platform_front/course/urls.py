from django.urls import path, include
from .views import courses, topics
from video import urls as video_urls

urlpatterns = [
    path('courses/', courses, name='courses'),  # Страница с курсами
    path('courses/<int:pk>/topics/', topics, name='topics'),  # Страница с темами курса
    path('courses/<int:pk>/topics/<int:topic_id>/', include(video_urls)),  # Маршрут для видео
]
