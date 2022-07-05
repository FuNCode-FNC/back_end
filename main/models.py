from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from .manager import CustomerManager
from django.db import models
from django.utils import timezone
from django.conf import settings


class Country(models.Model):
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    name = models.CharField('Страна производства', max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    name = models.CharField('Жанр', max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField('Категория', max_length=50)

    def __str__(self):
        return self.name


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField('username', max_length=256)
    firstName = models.CharField('Имя', max_length=256, null=True)
    secondName = models.CharField('Фамилия', max_length=256, null=True)
    is_active = models.BooleanField(default=True)
    account_type = models.CharField("Тип", max_length=30)
    admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomerManager()

    def has_perm(self, perm, obj=None):
        if self.admin:
            return True

    def has_module_perms(self, app_label):
        if self.admin:
            return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        if self.account_type == 'mod' or self.account_type == 'admin':
            return True
        return False

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class FilmAbstract(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=5000)
    kinopoisk_id = models.IntegerField(null=False)


class SerialAbstract(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=5000)
    kinopoisk_id = models.IntegerField(null=False)


class Comment(models.Model):
    author = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    rating = models.SmallIntegerField()
    to_film = models.ForeignKey(FilmAbstract, on_delete=models.CASCADE)
    to_serial = models.ForeignKey(SerialAbstract, on_delete=models.CASCADE)

    def check_comment(self):
        if Comment.to_film is None and Comment.to_serial is None:
            return False
        else:
            return True


class Film(models.Model):
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    year_of_release = models.IntegerField()
    date_of_adding = models.DateField(default=timezone.now)
    category = models.ManyToManyField(Category)
    genre = models.ManyToManyField(Genre)
    country = models.ManyToManyField(Country)
    person_who_added = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    screensaver_reference = models.URLField()
    magnet_reference = models.URLField()

    def __str__(self):
        return self.name
