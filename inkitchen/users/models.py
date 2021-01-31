from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth import get_user_model

import jwt
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class CustomUser(AbstractUser):
    """Кастомная модель Пользователя"""
    username = None
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True)
    about = models.TextField(max_length=300, verbose_name='О Себе', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

'''
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Определяет наш пользовательский класс User.
    Требуется адрес электронной почты и пароль.
    """

    username = None

    email = models.EmailField(_('email'), unique=True)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    # Свойство `USERNAME_FIELD` сообщает нам, какое поле мы будем использовать для входа.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Сообщает Django, что класс CustomUserManager должен управлять объектами этого типа.
    objects = CustomUserManager()

    def __str__(self):
        """
        Возвращает строковое представление этого `User`.
        Эта строка используется, когда в консоли выводится `User`.
        """
        return self.email

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Обычно это имя и фамилия пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его email.
        """
        return self.email

    def get_short_name(self):
        return self.email

    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

User = get_user_model()


class Customer(models.Model):       # покупатель

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True, null=True)
    geo_location = models.CharField(max_length=255, verbose_name='Местоположение', blank=True, null=True)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        db_table = 'Customer'

    def __str__(self):
        return 'Покупатель: {}'.format(self.user.email)


class Cook(models.Model):           # повар

    user = models.OneToOneField(User, verbose_name='Повар', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    kitchen = models.CharField(max_length=255, verbose_name='Кухня', blank=True, null=True)
    description = models.TextField(max_length=300, verbose_name='О поваре', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True, null=True)

    class Meta:
        verbose_name = 'Повар'
        verbose_name_plural = 'Повара'
        db_table = 'Cook'

    def __str__(self):
        return 'Повар: {}'.format(self.user.email)


class Doctor(models.Model):           # Врач

    user = models.OneToOneField(User, verbose_name='Врач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    description = models.TextField(max_length=300, verbose_name='О враче', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True, null=True)

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        db_table = 'Doctor'

    def __str__(self):
        return 'Врач: {}'.format(self.user.email)


class Nutritionist(models.Model):           # Диетолог

    user = models.OneToOneField(User, verbose_name='Диетолог', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    description = models.TextField(max_length=300, verbose_name='О диетологе', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True, null=True)

    class Meta:
        verbose_name = 'Диетолог'
        verbose_name_plural = 'Диетологи'
        db_table = 'Nutritionist'

    def __str__(self):
        return 'Диетолог: {}'.format(self.user.email)
        
'''