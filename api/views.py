from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import DayOfWeek, WorkSchedule, Booking
from .filters import BookingFilter, WorkScheduleFilter
from .serializers import DayOfWeekSerializer, WorkScheduleSerializer, BookingSerializer
from .paginations import StandartPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

class DayOfWeekViewSet(viewsets.ModelViewSet):
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer


class WorkScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandartPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WorkScheduleFilter

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            print(f"Ошибка в Perform_create: {e}")
            raise

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    pagination_class = StandartPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookingFilter

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(banker=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk)

            # Проверка прав доступа
            if not (request.user.is_superuser or request.user == booking.banker):
                return Response({'error': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)

            booking.confirmed = True
            booking.save()
            return Response({'status': 'Бронирование подтверждено'}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'error': 'Бронирование не найдено'}, status=status.HTTP_404_NOT_FOUND)

