
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='users/index.html'), name='home'),
    path('register', TemplateView.as_view(template_name='users/register.html'), name='register'),
    path('login', TemplateView.as_view(template_name='users/my-login.html'), name='my-login'),
    path('dashboard', TemplateView.as_view(template_name='users/dashboard.html'), name='dashboard'),
    path('profile', TemplateView.as_view(template_name='users/profile.html'), name='profile'),
    path('edit_profile', TemplateView.as_view(template_name='users/edit_profile.html'), name='edit_profile'),
    
]