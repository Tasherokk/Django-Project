# assistant/views.py
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ConversationHistory
from .serializers import ConversationHistorySerializer, UpdateAssistantResponseSerializer, CreateAssistantSerializer
from llama_index.agent.openai import OpenAIAssistantAgent
from rest_framework import viewsets, permissions, filters
from rest_framework_simplejwt.authentication import JWTAuthentication




# Создание нового взаимодействия с ассистентом
class CreateAssistantView(viewsets.ViewSet):
    serializer_class = CreateAssistantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        try:
            # Валидация данных через сериализатор
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            message = serializer.validated_data['message']
            print(message)

            # Создайте нового ассистента
            chatgpt_agent = OpenAIAssistantAgent.from_existing(
                assistant_id="asst_uu0ZuV4JXWGR1kJQMfeFe9gT",
                verbose=True,
            )
            print('aaaaa')
            response = chatgpt_agent.chat(message)
            # Сохраните историю разговора с обновленным thread_id
            ConversationHistory.objects.create(
                user_message=message,
                assistant_response=response.response,
                thread_id=chatgpt_agent.thread_id
            )
            return Response({
                "message": response.response,
                "thread_id": chatgpt_agent.thread_id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Обновление состояния ассистента и получение ответа
class UpdateAssistantResponseView(viewsets.ViewSet):
    serializer_class = UpdateAssistantResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        try:
            # Валидация данных через сериализатор
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            message = serializer.validated_data['message']
            thread_id = serializer.validated_data['thread_id']

            # Восстановите агент на основе ID и thread_id
            chatgpt_agent = OpenAIAssistantAgent.from_existing(
                assistant_id='asst_uu0ZuV4JXWGR1kJQMfeFe9gT',
                thread_id=thread_id,  # Используем thread_id для восстановления состояния
                verbose=True,
            )

            # Отправьте сообщение ассистенту и получите ответ
            response = chatgpt_agent.chat(message)

            # Сохраните историю разговора с обновленным thread_id
            ConversationHistory.objects.create(
                user_message=message,
                assistant_response=response.response,
                thread_id=thread_id
            )

            return Response({"response": response.response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Миксин для работы с историей
class ConversationHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = ConversationHistory.objects.all()
    serializer_class = ConversationHistorySerializer

    def get_queryset(self):
        """
        Фильтруем по assistant_id.
        """
        thread_id = self.kwargs.get('thread_id')
        if thread_id:
            return self.queryset.filter(thread_id=thread_id).order_by('timestamp')
        return self.queryset
