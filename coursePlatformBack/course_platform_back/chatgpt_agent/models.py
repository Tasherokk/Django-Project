# assistant/models.py
from django.db import models

class ConversationHistory(models.Model):
    user_message = models.TextField()
    assistant_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    thread_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Conversation with assistant {self.assistant_id} at {self.timestamp}"