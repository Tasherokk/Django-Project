# analytics/models.py

from django.contrib.auth.models import User
from django.db import models
from video.models import Video
from quiz.models import Test

class VideoView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_views')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_views')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['video']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} viewed {self.video.title} at {self.timestamp}"

class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_attempts')
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['test']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} scored {self.score} on {self.test.video.title} at {self.timestamp}"
