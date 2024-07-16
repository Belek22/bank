from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('profile/', views.RedactorProfileApiView.as_view({
        'get': 'get',
        'post': 'post',
        'put': 'put',
        'patch': 'patch',
    }),
    )
]