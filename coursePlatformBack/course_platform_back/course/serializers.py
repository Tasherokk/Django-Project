from rest_framework import serializers
from .models import Topic, Comment
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'course', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'course', 'author', 'created_at']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'course', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'course', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'course', 'author', 'created_at']