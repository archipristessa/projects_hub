from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    )

    email = models.EmailField(unique=True)
    patronymic = models.CharField(max_length=150, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class ProfileStudent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')

    # Академическая информация
    institute = models.CharField(max_length=255, blank=True, verbose_name='Институт/Факультет')
    course = models.PositiveSmallIntegerField(
        null=True,  # ВАЖНО: null=True для базы данных
        blank=True,  # ВАЖНО: blank=True для Django форм
        verbose_name='Курс',
        choices=[(i, f'{i} курс') for i in range(1, 7)]
    )
    group = models.CharField(max_length=50, blank=True, verbose_name='Группа')

    # Навыки и компетенции
    skills = models.TextField(blank=True, verbose_name='Навыки и компетенции')

    # Дополнительная информация
    bio = models.TextField(blank=True, verbose_name='О себе')

    # Контактная информация
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Telegram')
    github = models.URLField(blank=True, verbose_name='GitHub')
    portfolio = models.URLField(blank=True, verbose_name='Портфолио')

    def __str__(self):
        return f"Профиль студента: {self.user}"


class ProfileTeacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')

    # Профессиональная информация
    department = models.CharField(max_length=255, blank=True, verbose_name='Кафедра')
    position = models.CharField(max_length=255, blank=True, verbose_name='Должность')
    academic_degree = models.CharField(max_length=100, blank=True, verbose_name='Ученая степень')
    expertise = models.TextField(blank=True, verbose_name='Области экспертизы')
    bio = models.TextField(blank=True, verbose_name='Биография')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    office = models.CharField(max_length=100, blank=True, verbose_name='Кабинет')

    def __str__(self):
        return f"Профиль преподавателя: {self.user}"