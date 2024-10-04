from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Question, Answer


@api_view(['GET'])
def get_test(request):
    questions = Question.objects.prefetch_related('answers').all()
    data = []
    for question in questions:
        answers = question.answers.all()
        data.append({
            'id': question.id,
            'text': question.text,
            'answers': [{'id': answer.id, 'text': answer.text} for answer in answers]
        })
    return Response(data)

@api_view(['POST'])
def submit_test(request):
    user_answers = request.data.get('answers', {})
    score = 0
    for question_id, answer_id in user_answers.items():
        correct_answer = Answer.objects.filter(question_id=question_id, is_correct=True).first()
        if correct_answer and correct_answer.id == int(answer_id):
            score += 1
    return Response({'score': score})