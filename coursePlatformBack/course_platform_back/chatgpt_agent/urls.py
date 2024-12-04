# assistant/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateAssistantView, UpdateAssistantResponseView, ConversationHistoryViewSet
# Создание роутера
router = DefaultRouter()
router.register(r'conversation-history/(?P<thread_id>\w+)', ConversationHistoryViewSet, basename='conversation-history')

router.register(r'assistant/create', CreateAssistantView, basename='create_assistant')
router.register(r'assistant/update', UpdateAssistantResponseView, basename='update_assistant_response')

urlpatterns = [
    path('', include(router.urls)),  # Включаем роутер для conversation-history
]


