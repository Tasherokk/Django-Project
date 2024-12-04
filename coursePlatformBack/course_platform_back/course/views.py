# views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from rest_framework.exceptions import NotFound
from video.models import Video
from .models import Course, Topic  # Предположим, у вас есть модели Course и Topic
from rest_framework import generics, permissions
from .models import Topic, Comment
from .serializers import  CommentSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('platform')


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'  # This is the model field name (default is 'id')
    lookup_url_kwarg = 'comment_id'  # This is the URL keyword argument

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        logger.info(f"Fetching comments for course ID: {course_id}")
        return Comment.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        try:
            logger.info(f"Creating comment for course ID: {course_id}")
            course = Course.objects.get(id=course_id)
            serializer.save(author=self.request.user, course=course)
            logger.info("Comment created successfully")
        except Course.DoesNotExist:
            logger.error(f"Course with ID {course_id} not found")
            raise NotFound("Course not found")

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'id'  # Model field name
    lookup_url_kwarg = 'comment_id'  # URL keyword argument

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Comment.objects.filter(course_id=course_id)
    
#############################################################
def get_courses(request):
    logger.info("Fetching all courses")
    try:
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
        logger.debug(f"Found {len(course_data)} courses")
        return JsonResponse(course_data, safe=False)
    except Exception as e:
        logger.error(f"Error fetching courses: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def get_course(request, course_id):
    logger.info(f"Fetching course with ID: {course_id}")
    try:
        course = Course.objects.filter(id=course_id).first()
        if not course:
            logger.warning(f"Course with ID {course_id} not found")
            return JsonResponse({"error": "Course not found"}, status=404)

        course_data = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "created_at": course.created_at,
        }
        logger.debug(f"Course data: {course_data}")
        return JsonResponse(course_data, safe=False)
    except Exception as e:
        logger.error(f"Error fetching course with ID {course_id}: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def get_topics(request, course_id):
    logger.info(f"Fetching topics for course ID: {course_id}")
    try:
        topics = Topic.objects.filter(course_id=course_id)
        topic_data = [
            {"id": topic.id, "title": topic.title, "description": topic.description}
            for topic in topics
        ]
        logger.debug(f"Found {len(topic_data)} topics for course ID {course_id}")
        return JsonResponse(topic_data, safe=False)
    except Exception as e:
        logger.error(f"Error fetching topics for course ID {course_id}: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def get_videos(request, course_id, topic_id):
    logger.info(f"Fetching videos for topic ID: {topic_id}")
    try:
        videos = Video.objects.filter(topic_id=topic_id).values(
            "id", "title", "description", "image", "create_at"
        )
        video_list = list(videos)
        logger.debug(f"Found {len(video_list)} videos for topic ID {topic_id}")
        return JsonResponse(video_list, safe=False)
    except Exception as e:
        logger.error(f"Error fetching videos for topic ID {topic_id}: {e}")
        return JsonResponse({"error": str(e)}, status=500)


# @login_required
# @user_passes_test(lambda u: u.is_staff)
# def delete_comment(request, comment_id):
#     if request.method == 'DELETE':
#         try:
#             comment = Comment.objects.get(id=comment_id)
#             comment.delete()
#             return JsonResponse({'message': 'Comment deleted successfully.'})
#         except Comment.DoesNotExist:
#             return JsonResponse({'error': 'Comment not found.'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request method.'}, status=405)

class DeleteCommentView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)
