from course.models import Topic
from django.core.validators import FileExtensionValidator
from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="image/")
    file = models.FileField(
        upload_to="videos/",
        validators=[FileExtensionValidator(allowed_extensions=["mp4"])],
    )
    topic = models.ForeignKey(
        Topic, null=True, on_delete=models.CASCADE, related_name="videos"
    )
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
