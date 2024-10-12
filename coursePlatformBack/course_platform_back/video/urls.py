from django.urls import path
from . import views

urlpatterns = [
    path('api/stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('api/video/<int:pk>/', views.get_video, name='video'),
    path('api/videos/<int:topic_id>', views.get_list_video, name='video_list'),
]