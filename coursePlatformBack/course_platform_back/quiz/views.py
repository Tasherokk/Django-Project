from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from video.models import Video

from .models import Question, Test


@permission_classes([IsAuthenticated])
def get_test_for_video(request, video_id: int):
    test = get_object_or_404(Test, video_id=video_id)
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

    return JsonResponse(
        {
            "test": question_data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_questions(request):
    questions = Question.objects.all()
    data = []

    for question in questions:
        answer = question.answer
        data.append(
            {
                "id": question.id,
                "text": question.text,
                "answer": {
                    "option_1": answer.option_1,
                    "option_2": answer.option_2,
                    "option_3": answer.option_3,
                    "option_4": answer.option_4,
                    "correct_option": answer.correct_option,
                },
            }
        )

    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_test(request, video_id):
    try:
        data = request.data
        score = 0


        for question_id, selected_answer in data["answers"].items():
            question = get_object_or_404(
                Question, id=question_id
            )
            correct_answer = question.answer.correct_option
            if (
                int(selected_answer) == correct_answer
            ):
                score += 1

        return Response({"score": score})

    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=404)

    except KeyError:
        return Response({"error": "Invalid data format"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
