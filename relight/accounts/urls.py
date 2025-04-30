from django.urls import path, include
from .serializers import UserRegistrationSerializer
from . import views

#Urls
urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('auth/login/', views.LoginView.as_view()),
    path('auth/token/refresh/', views.RefreshTokenView.as_view()),
    path('auth/logout/', views.LogoutView.as_view()),
]