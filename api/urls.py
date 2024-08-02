from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DayOfWeekViewSet, WorkScheduleViewSet, BookingViewSet, BankersViewSet

router = DefaultRouter()
router.register('work-schedules', WorkScheduleViewSet)
router.register('bookings', BookingViewSet)
router.register('bankers', BankersViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('api.auth.urls')),
]
