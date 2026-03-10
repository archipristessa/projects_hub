from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Notification

User = get_user_model()


def create_notification(user, notification_type, message, project=None, application=None):
    """
    Создает уведомление для пользователя
    """
    with transaction.atomic():
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            message=message,
            related_project=project,
            related_application=application
        )
    return notification


def notify_new_application(application):
    """
    Уведомление автору проекта о новой заявке
    """
    project = application.project
    author = project.author

    message = f"Студент {application.applicant.get_full_name()} подал заявку на проект '{project.title}'"

    return create_notification(
        user=author,
        notification_type=Notification.NEW_APPLICATION,
        message=message,
        project=project,
        application=application
    )


def notify_application_status(application, status):
    """
    Уведомление студенту о решении по заявке
    """
    applicant = application.applicant
    project = application.project

    if status == 'accepted':
        notification_type = Notification.APPLICATION_ACCEPTED
        message = f"Поздравляем! Ваша заявка на проект '{project.title}' принята!"
    elif status == 'rejected':
        notification_type = Notification.APPLICATION_REJECTED
        message = f"Ваша заявка на проект '{project.title}' отклонена"
    else:
        print(f"ОШИБКА: неизвестный статус для уведомления: {status}")
        return None

    return create_notification(
        user=applicant,
        notification_type=notification_type,
        message=message,
        project=project,
        application=application
    )


def get_unread_count(user):
    """
    Получить количество непрочитанных уведомлений пользователя
    """
    return Notification.objects.filter(user=user, is_read=False).count()


def mark_all_as_read(user):
    """
    Пометить все уведомления пользователя как прочитанные
    """
    updated = Notification.objects.filter(
        user=user,
        is_read=False
    ).update(is_read=True)
    return updated


def mark_notifications_read_for_applications(user, applications):
    """
    Помечает уведомления как прочитанные для списка заявок
    """
    application_ids = list(applications.values_list('id', flat=True))

    Notification.objects.filter(
        user=user,
        related_application_id__in=application_ids,
        is_read=False
    ).update(is_read=True)