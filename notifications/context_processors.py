from .utils import get_unread_count


def notifications_count(request):
    """
    Добавляет количество непрочитанных уведомлений в контекст всех шаблонов
    """
    if request.user.is_authenticated:
        unread_count = get_unread_count(request.user)
        return {'unread_notifications_count': unread_count}
    return {}