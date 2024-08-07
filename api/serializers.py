from rest_framework import serializers
from core.models import DayOfWeek, WorkSchedule, Booking
from account.models import User
from datetime import date, datetime
import pytz


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
        try:
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
        except Exception as e:
            print(f"Ошибка в валидации: {e}")
            raise



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

        # Преобразование в offset-aware даты и времени
        now = utc.localize(datetime.now())
        if booking_start_time:
            booking_start_time = utc.localize(booking_start_time)
        booking_end_time = utc.localize(booking_end_time)

        # Проверка на прошедшие даты
        if booking_start_time and booking_start_time < now:
            raise serializers.ValidationError("Нельзя бронировать прошедшие даты.")
        if booking_end_time < now:
            raise serializers.ValidationError("Нельзя бронировать прошедшие даты.")

        # Проверка на выходные дни
        if booking_date.weekday() in [5, 6]:
            raise serializers.ValidationError("К сожалению, банкир в этот день отдыхает.")

        # Проверка на рабочее расписание банкира
        work_schedule = WorkSchedule.objects.filter(user=banker, date=booking_date).first()
        if not work_schedule:
            raise serializers.ValidationError("В этот день банкир не работает.")

        # Установка времени начала бронирования по умолчанию, если не указано
        if not booking_start_time:
            booking_start_time = datetime.combine(booking_date, work_schedule.start_time)
            booking_start_time = utc.localize(booking_start_time)
            data['booking_start_time'] = booking_start_time

        # Преобразование времени начала и конца работы банкира в offset-aware
        work_start_time = datetime.combine(booking_date, work_schedule.start_time)
        work_end_time = datetime.combine(booking_date, work_schedule.end_time)
        work_start_time = utc.localize(work_start_time)
        work_end_time = utc.localize(work_end_time)

        # Проверка на соответствие времени бронирования рабочему времени банкира
        if not (work_start_time <= booking_start_time <= work_end_time) or \
                not (work_start_time <= booking_end_time <= work_end_time):
            raise serializers.ValidationError("Время бронирования не соответствует рабочему времени банкира.")

        # Проверка пересечения с существующими бронированиями
        overlapping_bookings = Booking.objects.filter(
            banker=banker,
            booking_start_time__lt=booking_end_time,
            booking_end_time__gt=booking_start_time
        )
        if overlapping_bookings.exists():
            raise serializers.ValidationError("Банкир уже забронирован на это время.")

        return data

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)
