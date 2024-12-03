from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from video.models import Video

from .models import Question, Test
import logging

logger = logging.getLogger('platform')



@permission_classes([IsAuthenticated])
def get_test_for_video(request, video_id: int):
    logger.info(f"Fetching test for video ID: {video_id}")
    try:
        test = get_object_or_404(Test, video_id=video_id)
        questions = test.questions.prefetch_related("answer").all()
        logger.debug(f"Found {len(questions)} questions for video ID {video_id}")
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

        return JsonResponse({"test": question_data})
    except Test.DoesNotExist:
        logger.error(f"Test not found for video ID: {video_id}")
        return JsonResponse({"error": "Test not found"}, status=404)
    except Exception as e:
        logger.error(f"Error fetching test for video ID {video_id}: {e}")
        return JsonResponse({"error": str(e)}, status=500)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_questions(request):
    logger.info("Fetching all questions")
    try:
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
        logger.debug(f"Fetched {len(data)} questions")
        return Response(data)
    except Exception as e:
        logger.error(f"Error fetching questions: {e}")
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_test(request, video_id):
    logger.info(f"Submitting test for video ID: {video_id}")
    try:
        data = request.data
        logger.debug(f"Received data: {data}")
        score = 0

        for question_id, selected_answer in data["answers"].items():
            question = get_object_or_404(Question, id=question_id)
            correct_answer = question.answer.correct_option
            if int(selected_answer) == correct_answer:
                score += 1

        logger.info(f"Test submitted successfully for video ID {video_id}. Score: {score}")
        return Response({"score": score})

    except Question.DoesNotExist:
        logger.error(f"Question not found during test submission for video ID {video_id}")
        return Response({"error": "Question not found"}, status=404)

    except KeyError as e:
        logger.error(f"Invalid data format: {e}")
        return Response({"error": "Invalid data format"}, status=400)

    except Exception as e:
        logger.error(f"Error submitting test for video ID {video_id}: {e}")
        return Response({"error": str(e)}, status=500)
