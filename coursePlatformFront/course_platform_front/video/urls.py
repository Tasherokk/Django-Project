from django.urls import path

from . import views

urlpatterns = [
    path("videos/", views.video_list, name="videos"),  # Отображение всех видео для темы
    path(
        "videos/<int:video_id>/", views.video_detail, name="video_detail"
    ),  # Детальная страница для видео
]
