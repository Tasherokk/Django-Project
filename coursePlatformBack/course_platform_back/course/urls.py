# urls.py
from django.urls import path
from .views import get_courses, get_topics, get_videos,get_course,CommentListCreateAPIView,CommentDetailAPIView

urlpatterns = [
    path("api/courses/", get_courses, name="get_courses"),
    path("api/courses/<int:course_id>/topics/", get_topics, name="get_topics"),
    path("api/courses/<int:course_id>/", get_course, name="get_course"),

    path(
        "api/courses/<int:course_id>/topics/<int:topic_id>/videos",
        get_videos,
        name="get_videos",
    ),
    path("api/courses/<int:course_id>/comments/",CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path("api/courses/<int:course_id>/comments/<int:comment_id>", CommentDetailAPIView.as_view(), name='comment-detail'),

]