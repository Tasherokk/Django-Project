from django.urls import path
from .views import submit_test, get_questions, get_test_for_video

urlpatterns = [
    path('api/questions/', get_questions),
    path('api/test/<int:video_id>', get_test_for_video),
    path('api/submit_test/<int:video_id>', submit_test),
]
