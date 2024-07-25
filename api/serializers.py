from rest_framework import serializers
from core.models import DayOfWeek, WorkSchedule, Booking
from account.models import User
from datetime import date, datetime


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

        # Проверка пересечения с существующими расписаниями
        existing_schedules = WorkSchedule.objects.filter(user=user, date=schedule_date)
        for schedule in existing_schedules:
            if not (end_time <= schedule.start_time or start_time >= schedule.end_time):
                raise serializers.ValidationError("Расписание пересекается с существующим.")

        # Проверка на выходные дни
        if schedule_date.weekday() in [5, 6]:
            raise serializers.ValidationError("Нельзя добавлять расписание на выходные дни.")

        return data


class DateTimeFieldWithCustomFormat(serializers.DateTimeField):
    def to_internal_value(self, value):
        try:
            return datetime.strptime(value, '%d:%m:%Y %H:%M')
        except ValueError:
            raise serializers.ValidationError("Неверный формат даты и времени. Используйте формат 'День:Месяц:Год Время:Минуты'.")


class BookingSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    banker = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    booking_start_time = DateTimeFieldWithCustomFormat()
    booking_end_time = DateTimeFieldWithCustomFormat()

    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, data):
        booking_date = data.get('date')
        booking_start_datetime = data.get('booking_start_time')
        booking_end_datetime = data.get('booking_end_time')
        banker = data.get('banker')

        if not booking_start_datetime or not booking_end_datetime:
            raise serializers.ValidationError("Необходимо указать время начала и окончания бронирования.")

        booking_start_time = booking_start_datetime
        booking_end_time = booking_end_datetime

        # Проверка на прошедшие даты
        if booking_date < date.today():
            raise serializers.ValidationError("Нельзя бронировать прошедшие даты.")

        # Проверка на выходные дни
        if booking_date.weekday() in [5, 6]:
            raise serializers.ValidationError("К сожалению, банкир в этот день отдыхает.")

        # Проверка на рабочее расписание банкира
        work_schedule = WorkSchedule.objects.filter(user=banker, date=booking_date).first()
        if not work_schedule:
            raise serializers.ValidationError("В этот день банкир не работает.")

        # Установка времени начала бронирования по умолчанию, если не указано
        if booking_start_datetime is None:
            booking_start_datetime = datetime.combine(booking_date, work_schedule.start_time)
            data['booking_start_time'] = booking_start_datetime

        # Проверка на соответствие времени бронирования рабочему времени банкира
        if not (work_schedule.start_time <= booking_start_time.time() <= work_schedule.end_time) or \
                not (work_schedule.start_time <= booking_end_time.time() <= work_schedule.end_time):
            raise serializers.ValidationError("Время бронирования не соответствует рабочему времени банкира.")

        # Проверка пересечения с существующими бронированиями
        existing_bookings = Booking.objects.filter(banker=banker, date=booking_date)
        for booking in existing_bookings:
            if not (booking_end_time <= booking.booking_start_time or booking_start_time >= booking.booking_end_time):
                raise serializers.ValidationError("Банкир уже забронирован на это время.")

        return data
