from rest_framework import viewsets
from core.models import DayOfWeek, WorkSchedule, Booking
from .serializers import DayOfWeekSerializer, WorkScheduleSerializer, BookingSerializer

class DayOfWeekViewSet(viewsets.ModelViewSet):
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer
    permission_classes = []

class WorkScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
