from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Question
import json


# Обработка GET-запроса для получения вопросов и ответов
@api_view(['GET'])
def get_test(request):
    questions = Question.objects.all()
    data = []

    for question in questions:
        answer = question.answer
        data.append({
            'id': question.id,
            'text': question.text,
            'answer': {
                'option_1': answer.option_1,
                'option_2': answer.option_2,
                'option_3': answer.option_3,
                'option_4': answer.option_4,
                'correct_option': answer.correct_option,
            }
        })

    return Response(data)


# Обработка POST-запроса для отправки теста и расчета результата
@api_view(['POST'])
def submit_test(request):
    try:
        data = request.data  # Извлечение данных POST-запроса
        score = 0

        for question_id, selected_answer in data['answers'].items():
            question = Question.objects.get(id=question_id)
            correct_answer = question.answer.correct_option
            if int(selected_answer) == correct_answer:
                score += 1

        return Response({'score': score})

    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)

    except KeyError:
        return Response({'error': 'Invalid data format'}, status=400)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
