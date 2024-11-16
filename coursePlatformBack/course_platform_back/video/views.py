from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from quiz.models import Question  # Импортируй модель вопроса
from quiz.models import Test
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Video
from .services import open_file


def get_list_video(request, topic_id):
    videos = Video.objects.filter(topic_id=topic_id).values(
        "id", "title", "description", "image", "create_at"
    )
    return JsonResponse(list(videos), safe=False)


# @permission_classes([IsAuthenticated])
def get_video(request, pk: int):
    _video = get_object_or_404(Video, id=pk)
    test = get_object_or_404(Test, video=_video)
    questions = test.questions.prefetch_related("answer").all()
    question_data = []
    for question in questions:
        question_data.append(
            {
                "id": question.id,
                "text": question.text,
                "answer": {
                    "option_1": question.answer.option_1,
                    "option_2": question.answer.option_2,
                    "option_3": question.answer.option_3,
                    "option_4": question.answer.option_4,
                    "correct_option": question.answer.correct_option,
                },
            }
        )

    question_data = []
    for question in questions:
        question_data.append(
            {
                "id": question.id,
                "text": question.text,
                "answer": {
                    "option_1": question.answer.option_1,
                    "option_2": question.answer.option_2,
                    "option_3": question.answer.option_3,
                    "option_4": question.answer.option_4,
                },
            }
        )

    return JsonResponse(
        {
            "id": _video.id,
            "title": _video.title,
            "description": _video.description,
            "image": request.build_absolute_uri(_video.image.url),
            "create_at": _video.create_at,
            "questions": list(question_data),
        }
    )


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type="video/mp4")
    response["Accept-Ranges"] = "bytes"
    response["Content-Length"] = str(content_length)
    response["Cache-Control"] = "no-cache"
    response["Content-Range"] = content_range
    return response
