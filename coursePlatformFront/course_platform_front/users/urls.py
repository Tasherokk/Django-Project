
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user-logout', views.user_logout, name="user-logout"),

    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("edit/", views.edit_profile, name="edit_profile"),
    
]
# Beka password 12345Beka