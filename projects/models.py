from django.db import models
from users.models import User


class ProjectRole(models.Model):
    """Таблица командных ролей в проектах"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название роли')
    description = models.TextField(blank=True, verbose_name='Описание роли')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль в проекте'
        verbose_name_plural = 'Роли в проектах'


class Project(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активно ищет команду'),
        ('completed', 'Команда набрана'),
        ('archived', 'Архивирован'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_projects')
    title = models.CharField(max_length=255, verbose_name='Название проекта')
    description = models.TextField(verbose_name='Описание проекта')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    requirements = models.TextField(verbose_name='Требуемые роли и навыки')
    required_roles = models.ManyToManyField(ProjectRole, blank=True, verbose_name='Требуемые роли')  # Связь с ролями
    teacher_mentor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentored_projects',
        limit_choices_to={'user_type': 'teacher'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE,
                             verbose_name='Роль в проекте')  # Теперь ForeignKey к ProjectRole
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проектов'

    def __str__(self):
        return f"{self.user} в проекте {self.project} как {self.role}"