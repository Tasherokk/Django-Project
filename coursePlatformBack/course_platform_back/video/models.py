from django.db import models
from django.core.validators import FileExtensionValidator
class Video(models.Model):
    title= models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='image/')
    file=models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    create_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return self.title