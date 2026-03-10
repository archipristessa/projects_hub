from django.urls import path
from . import views

urlpatterns = [
    path('my-applications/', views.my_applications, name='my_applications'),
    path('project/<int:project_id>/apply/', views.create_application, name='create_application'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('<int:pk>/withdraw/', views.withdraw_application, name='withdraw_application'),
    path('project/<int:project_id>/applications/', views.project_applications, name='project_applications'),
    path('<int:pk>/status/<str:status>/', views.update_application_status, name='update_application_status'),
    path('<int:pk>/process/<str:action>/', views.process_application, name='process_application'),
    path('<int:pk>/applications/', views.project_applications, name='project_applications'),
]