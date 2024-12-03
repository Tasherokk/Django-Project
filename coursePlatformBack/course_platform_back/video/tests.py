# video/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from .models import Video
from course.models import Topic, Course
from quiz.models import Test, Question, Answer


class VideoAPITestCase(TestCase):
    def setUp(self):
        # Create an APIClient instance
        self.client = APIClient()

        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        # Create a course
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            # Include other required fields if any
        )

        # Create a topic associated with the course
        self.topic = Topic.objects.create(
            title='Test Topic',
            description='Test Topic Description',
            course=self.course
        )

        # Create dummy image and video files
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"image_content",
            content_type="image/jpeg"
        )

        video_file = SimpleUploadedFile(
            "test_video.mp4",
            b"video_content",
            content_type="video/mp4"
        )

        # Create a video associated with the topic
        self.video = Video.objects.create(
            title='Test Video',
            description='Test Video Description',
            image=image_file,
            file=video_file,
            topic=self.topic,
            create_at=timezone.now()
        )

        # Create a test associated with the video
        self.test = Test.objects.create(video=self.video)

        # Create a question
        self.question = Question.objects.create(
            text='Test Question'
        )

        # Create an answer associated with the question
        self.answer = Answer.objects.create(
            question=self.question,
            option_1='Option 1',
            option_2='Option 2',
            option_3='Option 3',
            option_4='Option 4',
            correct_option=1
        )

        # Add the question to the test
        self.test.questions.add(self.question)

    def test_get_list_video(self):
        url = reverse('video_list', kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        video_data = data[0]
        self.assertEqual(video_data['id'], self.video.id)
        self.assertEqual(video_data['title'], self.video.title)
        self.assertEqual(video_data['description'], self.video.description)
        self.assertIn('image', video_data)
        self.assertIn('create_at', video_data)

    def test_get_video(self):
        url = reverse('video', kwargs={'pk': self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        data = response.json()
        self.assertEqual(data['id'], self.video.id)
        self.assertEqual(data['title'], self.video.title)
        self.assertEqual(data['description'], self.video.description)
        self.assertIn('image', data)
        self.assertIn('create_at', data)
        self.assertIn('questions', data)
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions']), 1)

        question_data = data['questions'][0]
        self.assertEqual(question_data['id'], self.question.id)
        self.assertEqual(question_data['text'], self.question.text)
        self.assertIn('answer', question_data)
        answer_data = question_data['answer']
        self.assertEqual(answer_data['option_1'], self.answer.option_1)
        self.assertEqual(answer_data['option_2'], self.answer.option_2)
        self.assertEqual(answer_data['option_3'], self.answer.option_3)
        self.assertEqual(answer_data['option_4'], self.answer.option_4)
        # Depending on your view logic, 'correct_option' may or may not be included
        # If it's included, uncomment the next line
        # self.assertEqual(answer_data['correct_option'], self.answer.correct_option)

    def test_get_video_not_found(self):
        url = reverse('video', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_video_no_videos(self):
        # Create a new topic without videos
        new_topic = Topic.objects.create(
            title='New Topic',
            description='New Topic Description',
            course=self.course
        )
        url = reverse('video_list', kwargs={'topic_id': new_topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_get_streaming_video(self):
        url = reverse('stream', kwargs={'pk': self.video.id})
        # Mock the 'open_file' function if necessary
        response = self.client.get(url, HTTP_RANGE='bytes=0-1024')
        # The actual status code may vary depending on your 'open_file' implementation
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_206_PARTIAL_CONTENT])
        self.assertEqual(response['Content-Type'], 'video/mp4')
        self.assertIn('Content-Range', response)
        self.assertIn('Content-Length', response)

    def test_get_streaming_video_not_found(self):
        url = reverse('stream', kwargs={'pk': 9999})
        response = self.client.get(url, HTTP_RANGE='bytes=0-1024')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_video_without_test(self):
        # Create a video without an associated test
        image_file = SimpleUploadedFile(
            "test_image2.jpg",
            b"image_content",
            content_type="image/jpeg"
        )

        video_file = SimpleUploadedFile(
            "test_video2.mp4",
            b"video_content",
            content_type="video/mp4"
        )

        new_video = Video.objects.create(
            title='Test Video 2',
            description='Test Video Description 2',
            image=image_file,
            file=video_file,
            topic=self.topic,
            create_at=timezone.now()
        )

        url = reverse('video', kwargs={'pk': new_video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_video_unauthenticated(self):
        # If your view requires authentication, test unauthenticated access
        self.client.logout()
        url = reverse('video', kwargs={'pk': self.video.id})
        response = self.client.get(url)
        # Adjust expected status code based on your authentication settings
        # For example, 401 UNAUTHORIZED or 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Change if needed

    def test_get_list_video_unauthenticated(self):
        # Test unauthenticated access to the video list
        self.client.logout()
        url = reverse('video_list', kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Change if needed

    def test_get_streaming_video_unauthenticated(self):
        # Test unauthenticated access to streaming video
        self.client.logout()
        url = reverse('stream', kwargs={'pk': self.video.id})
        response = self.client.get(url, HTTP_RANGE='bytes=0-1024')
        # Adjust expected status code based on your authentication settings
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_206_PARTIAL_CONTENT])  # Change if needed
