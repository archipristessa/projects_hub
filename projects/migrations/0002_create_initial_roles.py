from django.db import migrations


def create_initial_roles(apps, schema_editor):
    ProjectRole = apps.get_model('projects', 'ProjectRole')

    # Список начальных ролей для проектов
    initial_roles = [
        ('Frontend Developer', 'Разработка пользовательского интерфейса на React, Vue, Angular'),
        ('Backend Developer', 'Разработка серверной части на Python, Java, Node.js'),
        ('Fullstack Developer', 'Полный цикл разработки - фронтенд и бэкенд'),
        ('UI/UX Designer', 'Дизайн интерфейсов и пользовательского опыта'),
        ('Project Manager', 'Управление проектом, командой и сроками'),
        ('Data Analyst', 'Анализ данных, статистика, визуализация'),
        ('Data Scientist', 'Машинное обучение, AI, продвинутая аналитика'),
        ('QA Engineer', 'Тестирование, обеспечение качества продукта'),
        ('DevOps Engineer', 'Развертывание, инфраструктура, CI/CD'),
        ('Mobile Developer', 'Разработка мобильных приложений'),
        ('Team Lead', 'Техническое руководство командой разработки'),
        ('Business Analyst', 'Анализ бизнес-требований и процессов'),
        ('Product Manager', 'Управление продуктом, стратегия развития'),
        ('Scrum Master', 'Координация agile-процессов в команде'),
        ('System Architect', 'Проектирование архитектуры системы'),
        ('Database Administrator', 'Администрирование и оптимизация БД'),
        ('Security Engineer', 'Информационная безопасность и защита данных'),
    ]

    for name, description in initial_roles:
        ProjectRole.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )


def reverse_roles(apps, schema_editor):
    ProjectRole = apps.get_model('projects', 'ProjectRole')
    ProjectRole.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_roles, reverse_roles),
    ]