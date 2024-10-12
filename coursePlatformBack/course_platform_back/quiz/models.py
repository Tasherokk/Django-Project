from django.db import models
from video.models import Video


class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_option = models.IntegerField(choices=[
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
    ])

    def __str__(self):
        return f"Answer for: {self.question.text}"


class Test(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='test')
    questions = models.ManyToManyField('Question')

    def __str__(self):
        return f"Test for {self.video.title}"
