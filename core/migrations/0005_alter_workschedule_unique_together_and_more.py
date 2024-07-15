# Generated by Django 5.0.6 on 2024-07-15 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_workschedule_day_of_week'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workschedule',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='booking',
            name='day_of_week',
            field=models.IntegerField(choices=[(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье')], default=0, verbose_name='День недели'),
        ),
        migrations.AlterField(
            model_name='workschedule',
            name='day_of_week',
            field=models.IntegerField(choices=[(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье')], default=0, verbose_name='День недели'),
        ),
    ]