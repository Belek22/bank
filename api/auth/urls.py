from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('profile/change_profile/<int:pk>/', views.RedactorProfileApiView.as_view()),
]