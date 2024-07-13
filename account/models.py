from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    CLIENT = 'client'
    BANKER = 'banker'
    ADMIN = 'admin'

    ROLE = (
        (CLIENT, 'Клиент'),
        (BANKER, 'Банкир'),
        (ADMIN, 'Администратор')
    )

    username = models.CharField(max_length=100, unique=True, verbose_name='никнейм')
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='аватарка')
    phone = PhoneNumberField(unique=True, verbose_name='номер телефона')
    email = models.EmailField(null=True, verbose_name='электронная почта', unique=True)
    role = models.CharField('роль', choices=ROLE, default=CLIENT, max_length=15)
    experience = models.PositiveIntegerField(verbose_name='опыт работы', null=True, blank=True)
    position = models.CharField(max_length=155, verbose_name='должность', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'
