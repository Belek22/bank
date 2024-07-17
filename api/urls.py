from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DayOfWeekViewSet, WorkScheduleViewSet, BookingViewSet

router = DefaultRouter()
router.register('dayofweek', DayOfWeekViewSet)
router.register('workschedule', WorkScheduleViewSet)
router.register('booking', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('api.auth.urls'))
]
