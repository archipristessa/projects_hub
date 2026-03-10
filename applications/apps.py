from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications'

    def ready(self):
        # Регистрируем сигналы при загрузке приложения
        import applications.signals