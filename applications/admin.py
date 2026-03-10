from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'project', 'applied_role', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'applied_role')
    search_fields = ('applicant__first_name', 'applicant__last_name', 'project__title')
    readonly_fields = ('created_at', 'updated_at')