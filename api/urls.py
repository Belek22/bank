# core/urls.py
from django.urls import path, include
from .views import DayOfWeekListCreateAPIView, WorkScheduleListCreateAPIView, BookingListCreateAPIView, BookingDetailAPIView

urlpatterns = [
    path('daysofweek/', DayOfWeekListCreateAPIView.as_view(), name='dayofweek-list-create'),
    path('workschedules/', WorkScheduleListCreateAPIView.as_view(), name='workschedule-list-create'),
    path('bookings/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path("auth/", include('api.auth.urls')),
]
