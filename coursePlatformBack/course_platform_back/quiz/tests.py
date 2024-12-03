# quiz/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from .models import Question, Answer, Test
from video.models import Video
from django.core.files.uploadedfile import SimpleUploadedFile
from course.models import Course, Topic

class QuizAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.client.force_authenticate(user=self.user)
        self.client.login(username='testuser', password='testpass')

        # Create a course
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            # Add other required fields if any
        )

        # Create a topic associated with the course
        self.topic = Topic.objects.create(
            title='Test Topic',
            description='Test Topic Description',
            course=self.course  # Assign the course
        )

        # Create a dummy file for the video
        test_file = SimpleUploadedFile(
            "test_video.mp4",
            b"file_content",
            content_type="video/mp4"
        )

        # Create a video associated with the topic
        self.video = Video.objects.create(
            title='Test Video',
            description='Test Description',
            file=test_file,
            topic=self.topic  # ForeignKey field
        )

        # Create a test associated with the video
        self.test = Test.objects.create(video=self.video)

        self.question1 = Question.objects.create(
            text='Test Question 1',
        )

        # Create an answer
        self.answer1 = Answer.objects.create(
            question=self.question1,
            option_1='Option 1',
            option_2='Option 2',
            option_3='Option 3',
            option_4='Option 4',
            correct_option=1
        )

        self.test.questions.add(self.question1)


    def test_get_questions(self):
        url = reverse('get_questions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        self.assertEqual(len(response.data), 1)
        question_data = response.data[0]
        self.assertEqual(question_data['id'], self.question1.id)
        self.assertEqual(question_data['text'], self.question1.text)
        self.assertIn('answer', question_data)
        answer_data = question_data['answer']
        self.assertEqual(answer_data['option_1'], self.answer1.option_1)
        self.assertEqual(answer_data['option_2'], self.answer1.option_2)
        self.assertEqual(answer_data['option_3'], self.answer1.option_3)
        self.assertEqual(answer_data['option_4'], self.answer1.option_4)
        self.assertEqual(answer_data['correct_option'], self.answer1.correct_option)

    def test_get_test_for_video(self):
        url = reverse('get_test_for_video', kwargs={'video_id': self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        test_data = response.json()
        self.assertIn('test', test_data)
        self.assertEqual(len(test_data['test']), 1)
        question_data = test_data['test'][0]
        self.assertEqual(question_data['id'], self.question1.id)
        self.assertEqual(question_data['text'], self.question1.text)
        self.assertIn('answer', question_data)
        answer_data = question_data['answer']
        self.assertEqual(answer_data['option_1'], self.answer1.option_1)
        self.assertEqual(answer_data['option_2'], self.answer1.option_2)
        self.assertEqual(answer_data['option_3'], self.answer1.option_3)
        self.assertEqual(answer_data['option_4'], self.answer1.option_4)
        self.assertEqual(answer_data['correct_option'], self.answer1.correct_option)

    def test_get_test_for_video_not_found(self):
        url = reverse('get_test_for_video', kwargs={'video_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_submit_test(self):
        url = reverse('submit_test', kwargs={'video_id': self.video.id})
        data = {
            "answers": {
                str(self.question1.id): str(self.answer1.correct_option)
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('score', response.data)
        self.assertEqual(response.data['score'], 1)

    def test_submit_test_incorrect_answer(self):
        url = reverse('submit_test', kwargs={'video_id': self.video.id})
        data = {
            "answers": {
                str(self.question1.id): "2"  # Assuming correct_option is 1
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('score', response.data)
        self.assertEqual(response.data['score'], 0)

    def test_submit_test_invalid_data(self):
        url = reverse('submit_test', kwargs={'video_id': self.video.id})
        data = {}  # Missing 'answers' key
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_questions_unauthenticated(self):
        self.client.logout()
        url = reverse('get_questions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_test_for_video_unauthenticated(self):
        self.client.logout()
        url = reverse('get_test_for_video', kwargs={'video_id': self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_submit_test_unauthenticated(self):
        self.client.logout()
        url = reverse('submit_test', kwargs={'video_id': self.video.id})
        data = {
            "answers": {
                str(self.question1.id): str(self.answer1.correct_option)
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

