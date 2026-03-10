from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification
from .utils import mark_all_as_read


class NotificationListView(LoginRequiredMixin, ListView):
    """
    Страница со списком всех уведомлений пользователя
    """
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            mark_all_as_read(request.user)
        return super().get(request, *args, **kwargs)


@login_required
def notification_detail(request, pk):
    """
    Просмотр деталей уведомления
    """
    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    notification.mark_as_read()

    if notification.related_project:
        return redirect('project_detail', pk=notification.related_project.pk)
    elif notification.related_application:
        return redirect('application_detail', pk=notification.related_application.pk)

    return redirect('notifications:list')


@login_required
def mark_all_notifications_read(request):
    """
    API endpoint для пометки всех уведомлений как прочитанных
    """
    mark_all_as_read(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'notifications:list'))

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET"])
def unread_notifications_count(request):
    """Возвращает количество непрочитанных уведомлений для AJAX"""
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})

@login_required
@require_http_methods(["POST"])
def mark_notification_read(request, pk):
    """Помечает уведомление как прочитанное через AJAX"""
    from .models import Notification
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    return JsonResponse({'success': True})