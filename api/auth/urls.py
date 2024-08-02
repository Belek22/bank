from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .import views
from .views import UserProfileViewSet, BankerViewSet

router = DefaultRouter()
router.register(r'user-profile', UserProfileViewSet)
router.register(r'bankers', BankerViewSet)

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('profile/', views.RedactorProfileApiView.as_view({
        'get': 'get',
        'post': 'post',
        'put': 'put',
        'patch': 'patch',
    })),
    path('', include(router.urls)),
]