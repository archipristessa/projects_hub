from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/my-projects/', views.my_projects, name='my_projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('projects/<int:pk>/apply/', views.apply_to_project, name='apply_to_project'),
    path('projects/roles/', views.project_roles_list, name='project_roles_list'),


]