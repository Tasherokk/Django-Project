from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, EditProfileView, UserDetailsView

urlpatterns = [
    path('api/users/register/', RegisterView.as_view(), name='api-register'),
    path('api/users/login/', LoginView.as_view(), name='api-login'),
    path('api/users/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/users/profile/<str:username>/', ProfileView.as_view(), name='api-profile'),
    path('api/users/profile/edit/<int:pk>/', EditProfileView.as_view(), name='api-edit-profile'),
    path('api/users/me/', UserDetailsView.as_view(), name='user-details'),

]
