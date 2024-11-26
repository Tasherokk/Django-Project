# views.py
from django.http import JsonResponse
from video.models import Video
from .models import Course, Topic  # Предположим, у вас есть модели Course и Topic
from rest_framework import generics, permissions
from .models import Topic, Comment
from .serializers import  CommentSerializer
from .permissions import IsAuthorOrReadOnly

class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Comment.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id)
        serializer.save(author=self.request.user, course=course)

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Comment.objects.filter(course_id=course_id)
    
#############################################################
def get_courses(request):
    courses = Course.objects.all()
    course_data = [
        {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "created_at": course.created_at,
        }
        for course in courses
    ]
    return JsonResponse(course_data, safe=False)

def get_course(request,course_id):
    course = Course.objects.filter(id=course_id).first()
    print(course)
    course_data = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "created_at": course.created_at,
        }
    
    return JsonResponse(course_data, safe=False)


def get_topics(request, course_id):
    topics = Topic.objects.filter(course_id=course_id)
    topic_data = [
        {"id": topic.id, "title": topic.title, "description": topic.description}
        for topic in topics
    ]
    return JsonResponse(topic_data, safe=False)


def get_videos(request, topic_id):
    videos = Video.objects.filter(topic_id=topic_id).values(
        "id", "title", "description", "image", "create_at"
    )
    return JsonResponse(list(videos), safe=False)
