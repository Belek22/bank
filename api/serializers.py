# core/serializers.py
from rest_framework import serializers
from core.models import DayOfWeek, WorkSchedule, Booking
from account.models import User

class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = '__all__'

class WorkScheduleSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    day_of_week = DayOfWeekSerializer()

    class Meta:
        model = WorkSchedule
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    banker = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Booking
        fields = "__all__"
