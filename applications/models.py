from django.db import models
from users.models import User
from projects.models import Project, ProjectRole


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Рассматривается'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField(blank=True, verbose_name='Сопроводительное письмо')
    applied_role = models.ForeignKey(ProjectRole, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Роль, на которую претендует')  # Теперь ForeignKey
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'applicant')
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f"Заявка {self.applicant} на {self.project} как {self.applied_role}"