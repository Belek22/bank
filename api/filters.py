import django_filters
from django_filters import rest_framework as filters
from core.models import WorkSchedule, Booking

class WorkScheduleFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='date', lookup_expr='exact')
    start_time = filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = filters.TimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = WorkSchedule
        fields = ['date', 'start_time', 'end_time']

class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = {
            'client': ['exact'],
            'banker': ['exact'],
            'date': ['exact', 'gte', 'lte'],
            'confirmed': ['exact'],
        }
