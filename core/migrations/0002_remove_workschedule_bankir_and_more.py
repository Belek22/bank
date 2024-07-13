# Generated by Django 5.0.6 on 2024-07-13 07:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workschedule',
            name='bankir',
        ),
        migrations.RemoveField(
            model_name='workschedule',
            name='on_off',
        ),
        migrations.AlterField(
            model_name='workschedule',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_schedule', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField(verbose_name='Дата бронирования')),
                ('booking_start_time', models.TimeField(verbose_name='Время начала бронирования')),
                ('booking_end_time', models.TimeField(verbose_name='Время окончания бронирования')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Подтверждено')),
                ('banker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_by', to=settings.AUTH_USER_MODEL, verbose_name='Банкир')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
    ]
