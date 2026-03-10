from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Application
import logging
logger = logging.getLogger(__name__)
try:
    from notifications.utils import notify_new_application, notify_application_status, create_notification

    NOTIFICATIONS_ENABLED = True
except ImportError:
    NOTIFICATIONS_ENABLED = False


@receiver(post_save, sender=Application)
def handle_application_save(sender, instance, created, **kwargs):
    """
    Автоматически отправляет уведомления при создании/изменении заявки
    """
    if not NOTIFICATIONS_ENABLED:
        return
    if created and hasattr(instance, '_skip_notification'):
        return
    if created:
        # Новая заявка → уведомляем автора проекта
        notify_new_application(instance)

    elif 'update_fields' in kwargs and kwargs['update_fields']:
        # Если изменился статус заявки
        if 'status' in kwargs['update_fields']:
            if instance.status == 'accepted':
                notify_application_status(instance, 'accepted')
            elif instance.status == 'rejected':
                notify_application_status(instance, 'rejected')


@receiver(post_delete, sender=Application)
def handle_application_delete(sender, instance, **kwargs):
    """
    Уведомляем автора проекта об отзыве заявки
    """
    if not NOTIFICATIONS_ENABLED:
        return

    try:
        create_notification(
            user=instance.project.author,
            notification_type='application_withdrawn',
            message=f'Студент {instance.applicant.get_full_name()} отозвал заявку на проект "{instance.project.title}"',
            project=instance.project
        )
    except Exception as e:
        logger.error(f"Ошибка уведомления об отзыве: {e}",
                    exc_info=True,
                    extra={'application_id': instance.id})