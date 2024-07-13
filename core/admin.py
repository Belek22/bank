from django.contrib import admin
from .models import DayOfWeek, WorkSchedule, Booking

@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('day',)

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'banker', 'booking_start_time', 'booking_end_time', 'confirmed')

    def client(self, obj):
        return obj.client.get_full_name()

    def banker(self, obj):
        return obj.banker.get_full_name()