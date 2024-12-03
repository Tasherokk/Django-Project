# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Topic, Comment
from users.models import User
from video.models import Video
from .permissions import IsAuthorOrReadOnly


class CommentListCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.client.login(username='testuser', password='testpass')

        # Create a course
        self.course = Course.objects.create(title='Test Course', description='Description')
        self.comment_url = f'/course/api/courses/{self.course.id}/comments/'

    def test_list_comments(self):
        # Create comments
        Comment.objects.create(course=self.course, author=self.user, content='Comment 1')
        Comment.objects.create(course=self.course, author=self.user, content='Comment 2')

        response = self.client.get(self.comment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_comment(self):
        data = {'content': 'This is a test comment'}
        response = self.client.post(self.comment_url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Response status code:", response.status_code)
            print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'This is a test comment')


class CommentDetailAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create users
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.login(username='testuser', password='testpass')

        # Create a course and comment
        self.course = Course.objects.create(title='Test Course', description='Course Description')
        self.comment = Comment.objects.create(course=self.course, author=self.user, content='Test Comment')
        self.detail_url = f'/course/api/courses/{self.course.id}/comments/{self.comment.id}'

        # Authenticate as the author
        self.client.force_authenticate(user=self.user)

    def test_retrieve_comment(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test Comment')

    def test_update_comment(self):
        data = {'content': 'Updated Comment'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated Comment')

    def test_delete_comment(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_update_comment_by_non_author(self):
        # Authenticate as a different user
        self.client.force_authenticate(user=self.other_user)
        data = {'content': 'Malicious Update'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_by_non_author(self):
        # Authenticate as a different user
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetCoursesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Course.objects.create(title='Course 1', description='Description 1')
        Course.objects.create(title='Course 2', description='Description 2')
        self.url = '/course/api/courses/'

    def test_get_courses(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)


class GetCourseTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(title='Course 1', description='Description 1')
        self.url = f'/course/api/courses/{self.course.id}/'

    def test_get_course(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['title'], 'Course 1')
        self.assertEqual(data['description'], 'Description 1')

    def test_get_nonexistent_course(self):
        response = self.client.get('/course/api/courses/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetTopicsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(title='Course 1', description='Description 1')
        Topic.objects.create(course=self.course, title='Topic 1', description='Description 1')
        Topic.objects.create(course=self.course, title='Topic 2', description='Description 2')
        self.url = f'/course/api/courses/{self.course.id}/topics/'

    def test_get_topics(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)


class GetVideosTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create course and topic
        self.course = Course.objects.create(title='Course 1', description='Description 1')
        self.topic = Topic.objects.create(course=self.course, title='Topic 1', description='Description 1')

        # Create videos
        Video.objects.create(topic=self.topic, title='Video 1', description='Description 1', image='image1.png')
        Video.objects.create(topic=self.topic, title='Video 2', description='Description 2', image='image2.png')

        self.url = f'/course/api/courses/{self.course.id}/topics/{self.topic.id}/videos'

    def test_get_videos(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
