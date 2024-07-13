from rest_framework import generics
from core.models import DayOfWeek, WorkSchedule, Booking
from .serializers import DayOfWeekSerializer, WorkScheduleSerializer, BookingSerializer

class DayOfWeekListCreateAPIView(generics.ListCreateAPIView):
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer

class WorkScheduleListCreateAPIView(generics.ListCreateAPIView):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer

class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


