from django.db import models

class ConversationHistory(models.Model):
    user_message = models.TextField()
    assistant_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    thread_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),  # Индекс для сортировки по времени
            models.Index(fields=["thread_id"]),  # Индекс для быстрого поиска по thread_id
        ]

    def __str__(self):
        return f"Conversation at {self.timestamp}"