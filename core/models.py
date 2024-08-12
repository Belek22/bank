from django.db import models
from account.models import User

class DayOfWeek(models.Model):
    day_choices = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )
    day = models.IntegerField(choices=day_choices, unique=True, verbose_name='День недели')

    class Meta:
        verbose_name = 'Рабочий день недели'
        verbose_name_plural = 'Рабочие дни недели'
        ordering = ['day']

    def __str__(self):
        return self.get_day_display()

DAY_CHOICES = (
    (0, 'Понедельник'),
    (1, 'Вторник'),
    (2, 'Среда'),
    (3, 'Четверг'),
    (4, 'Пятница'),
)


class WorkSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Банкир')
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Начало работы')
    end_time = models.TimeField(verbose_name='Конец работы')
    end_of_work_week = models.DateField()

    class Meta:
        verbose_name = 'Расписание работы'
        verbose_name_plural = 'Расписания работы'

    def __str__(self):
        return f'{self.user} работает {self.date} с {self.start_time} до {self.end_time}'



class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name='Клиент')
    banker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_by', verbose_name='Банкир')
    booking_start_time = models.DateTimeField(verbose_name='Время начала бронирования')
    booking_end_time = models.DateTimeField(verbose_name='Время окончания бронирования')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'{self.client} бронирует {self.banker} с {self.booking_start_time} до {self.booking_end_time}'
