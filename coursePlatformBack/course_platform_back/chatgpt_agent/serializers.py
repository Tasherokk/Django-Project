# assistant/serializers.py
from rest_framework import serializers
from .models import ConversationHistory

class ConversationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationHistory
        fields = ['timestamp', 'user_message', 'assistant_response']

class CreateAssistantSerializer(serializers.Serializer):
    message = serializers.CharField()

class UpdateAssistantResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    thread_id = serializers.CharField()