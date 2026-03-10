from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProfileStudent, ProfileTeacher

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'patronymic', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'patronymic', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'patronymic', 'user_type'),
        }),
    )

@admin.register(ProfileStudent)
class ProfileStudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'institute', 'course', 'group')  # то что отображается в админке
    list_filter = ('institute', 'course')  # то по каким полям возможна фильтрация
    search_fields = ('user__first_name', 'user__last_name', 'institute', 'group')
    fieldsets = (
        ('Основная информация', {
            'fields': ('user',)
        }),
        ('Академическая информация', {
            'fields': ('institute', 'course', 'group')
        }),
        ('Навыки и компетенции', {
            'fields': ('skills',)
        }),
        ('Контактная информация', {
            'fields': ('phone', 'telegram', 'github', 'portfolio'),
            'classes': ('collapse',)
        }),
        ('Дополнительная информация', {
            'fields': ('bio',)
        }),
    )
    # Убрали readonly_fields так как у нас больше нет created_at и updated_at

@admin.register(ProfileTeacher)
class ProfileTeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'academic_degree')  # Убрали created_at
    list_filter = ('department',)  # Убрали created_at
    search_fields = ('user__first_name', 'user__last_name', 'department')
    fieldsets = (
        ('Основная информация', {
            'fields': ('user',)
        }),
        ('Профессиональная информация', {
            'fields': ('department', 'position', 'academic_degree')
        }),
        ('Экспертиза', {
            'fields': ('expertise',)
        }),
        ('Контактная информация', {
            'fields': ('phone', 'office'),
            'classes': ('collapse',)
        }),
        ('Биография', {
            'fields': ('bio',)
        }),
    )
