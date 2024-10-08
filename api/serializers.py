from rest_framework import serializers
from core.models import DayOfWeek, WorkSchedule, Booking
from account.models import User
from datetime import datetime
import pytz
from django.db import transaction

class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = '__all__'


class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        schedule_date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        end_of_work_week = data.get('end_of_work_week')

        existing_schedules = WorkSchedule.objects.filter(user=user, date=schedule_date)
        for schedule in existing_schedules:
            if not (end_time <= schedule.start_time or start_time >= schedule.end_time):
                raise serializers.ValidationError("Расписание пересекается с существующим.")

        if schedule_date.weekday() in [5, 6]:
            raise serializers.ValidationError("Нельзя добавлять расписание на выходные дни.")

        if end_of_work_week and end_of_work_week < schedule_date:
            raise serializers.ValidationError("Дата окончания рабочей недели не может быть раньше даты расписания.")

        return data


class DateTimeFieldWithCustomFormat(serializers.DateTimeField):
    def to_internal_value(self, value):
        try:
            return datetime.strptime(value, '%d:%m:%Y %H:%M')
        except ValueError:
            raise serializers.ValidationError("Неверный формат даты и времени. Используйте формат 'День:Месяц:Год Часы:Минуты'.")


class BookingSerializer(serializers.ModelSerializer):
    banker = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    booking_start_time = DateTimeFieldWithCustomFormat(required=False)
    booking_end_time = DateTimeFieldWithCustomFormat()

    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, data):
        booking_start_time = data.get('booking_start_time')
        booking_end_time = data.get('booking_end_time')
        banker = data.get('banker')

        if not booking_end_time:
            raise serializers.ValidationError("Необходимо указать время окончания бронирования.")

        booking_date = booking_end_time.date()
        utc = pytz.UTC
        now = utc.localize(datetime.now())

        if booking_start_time:
            booking_start_time = utc.localize(booking_start_time)
        booking_end_time = utc.localize(booking_end_time)

        if booking_start_time and booking_start_time < now:
            raise serializers.ValidationError("Нельзя бронировать прошедшие даты.")
        if booking_end_time < now:
            raise serializers.ValidationError("Нельзя бронировать прошедшие даты.")

        # Фильтрация расписания по дате и диапазону рабочей недели
        work_schedule = WorkSchedule.objects.filter(
            user=banker,
            date__lte=booking_date,
            end_of_work_week__gte=booking_date
        ).first()

        if not work_schedule:
            raise serializers.ValidationError("В этот день банкир не работает.")

        # Определение времени начала и конца работы
        if not booking_start_time:
            booking_start_time = datetime.combine(booking_date, work_schedule.start_time)
            booking_start_time = utc.localize(booking_start_time)
            data['booking_start_time'] = booking_start_time

        work_start_time = utc.localize(datetime.combine(booking_date, work_schedule.start_time))
        work_end_time = utc.localize(datetime.combine(booking_date, work_schedule.end_time))

        if not (work_start_time <= booking_start_time <= work_end_time) or \
                not (work_start_time <= booking_end_time <= work_end_time):
            raise serializers.ValidationError("Время бронирования не соответствует рабочему времени банкира.")

        # Проверка на конец рабочей недели
        if booking_end_time.date() > work_schedule.end_of_work_week:
            raise serializers.ValidationError("Бронирование не может выходить за пределы рабочей недели.")

        # Проверка на перекрывающиеся бронирования
        overlapping_bookings = Booking.objects.filter(
            banker=banker,
            booking_start_time__lt=booking_end_time,
            booking_end_time__gt=booking_start_time
        )
        if overlapping_bookings.exists():
            raise serializers.ValidationError("Банкир уже забронирован на это время.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user

        banker = validated_data['banker']
        booking_start_time = validated_data['booking_start_time']
        booking_end_time = validated_data['booking_end_time']

        overlapping_bookings = Booking.objects.select_for_update().filter(
            banker=banker,
            booking_start_time__lt=booking_end_time,
            booking_end_time__gt=booking_start_time
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Банкир уже забронирован на это время.")

        return super().create(validated_data)
