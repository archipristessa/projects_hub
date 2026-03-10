# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    """
    Модель для хранения уведомлений пользователей
    """
    # Типы уведомлений
    NEW_APPLICATION = 'new_application'
    APPLICATION_ACCEPTED = 'application_accepted'
    APPLICATION_REJECTED = 'application_rejected'

    NOTIFICATION_TYPES = (
        (NEW_APPLICATION, 'Новая заявка на ваш проект'),
        (APPLICATION_ACCEPTED, 'Ваша заявка принята'),
        (APPLICATION_REJECTED, 'Ваша заявка отклонена'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Пользователь'
    )

    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES,
        verbose_name='Тип уведомления'
    )

    message = models.TextField(verbose_name='Сообщение')

    related_project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанный проект'
    )

    related_application = models.ForeignKey(
        'applications.Application',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная заявка'
    )

    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.email}: {self.get_notification_type_display()} ({'не прочитано' if not self.is_read else 'прочитано'})"

    def mark_as_read(self):
        """Пометить уведомление как прочитанное"""
        self.is_read = True
        self.save(update_fields=['is_read'])