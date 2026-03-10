from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from projects import views as project_views
from django.views.generic import TemplateView

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница
    path('', project_views.home_page, name='home'),
    path('', include('projects.urls')),
    # Включаем users URLs с префиксом users/
    path('users/', include('users.urls')),
    path('applications/', include('applications.urls')),
    path('notifications/', include('notifications.urls')),
    # Остальные страницы
    #path('projects/', TemplateView.as_view(template_name='projects/list.html'), name='project-list-page'),
    #path('projects/<int:pk>/', TemplateView.as_view(template_name='projects/detail.html'), name='project_detail'),
    #path('my-projects/', TemplateView.as_view(template_name='my_projects.html'), name='my-projects'),
    #path('my-applications/', TemplateView.as_view(template_name='my_applications.html'), name='my-applications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)