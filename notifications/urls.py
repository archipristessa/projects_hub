from django.urls import path
from . import views

app_name = 'notifications'


urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),
    path('<int:pk>/', views.notification_detail, name='detail'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark_all_read'),
    path('unread-count/', views.unread_notifications_count, name='unread_count'),
    path('<int:pk>/mark-read/', views.mark_notification_read, name='mark_read'),
]