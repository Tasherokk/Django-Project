from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from course.models import Course

def dashboard(request):
    # Annotate courses with aggregated data
    courses = Course.objects.annotate(
        num_topics=Count('topics', distinct=True),
        num_videos=Count('topics__videos', distinct=True),
        num_tests=Count('topics__videos__test', distinct=True),
        num_questions=Count('topics__videos__test__questions', distinct=True),
        num_comments=Count('comments', distinct=True)

    )

    # Prepare data for charts
    course_titles = [course.title for course in courses]
    num_topics = [course.num_topics for course in courses]
    num_videos = [course.num_videos for course in courses]
    num_tests = [course.num_tests for course in courses]
    num_questions = [course.num_questions for course in courses]
    num_comments = [course.num_comments for course in courses]

    # Pass data to the template
    context = {
        'course_titles': course_titles,
        'num_topics': num_topics,
        'num_videos': num_videos,
        'num_tests': num_tests,
        'num_questions': num_questions,
        'num_comments': num_comments,

    }

    return render(request, 'dashboard.html', context)