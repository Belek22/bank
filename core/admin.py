from django.contrib import admin
from .models import WorkSchedule, Booking

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time')
    list_display_links = ('user', 'day_of_week')
    search_fields = ('user', 'day_of_week')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'banker', 'booking_start_time', 'booking_end_time', 'confirmed')
    list_display_links = ('client', 'banker')
    search_fields = ('client', 'banker')

    def client(self, obj):
        return obj.client.get_full_name()

    def banker(self, obj):
        return obj.banker.get_full_name()