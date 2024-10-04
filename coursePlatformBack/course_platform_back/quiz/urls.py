from django.urls import path
from .views import get_test, submit_test

urlpatterns = [
    path('test/', get_test),
    path('submit/', submit_test),
]
