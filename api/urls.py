from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import DayOfWeekViewSet, WorkScheduleViewSet, BookingViewSet

router = DefaultRouter()
router.register('work-schedules', WorkScheduleViewSet)
router.register('bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('api.auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token),
]
