from django.contrib import admin
from .models import ProjectRole, Project, ProjectMember

@admin.register(ProjectRole)
class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'required_roles')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    filter_horizontal = ('required_roles',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__first_name', 'user__last_name', 'project__title')