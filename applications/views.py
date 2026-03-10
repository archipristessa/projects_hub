from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Application, Project

try:
    from notifications.utils import notify_new_application, notify_application_status
    NOTIFICATIONS_ENABLED = True
except ImportError:
    NOTIFICATIONS_ENABLED = False
    print("Предупреждение: Приложение 'notifications' не установлено. Уведомления отключены.")
@login_required
def create_application(request, project_id):
    """Подача заявки на проект"""
    project = get_object_or_404(Project, pk=project_id)

    # Проверяем, не является ли пользователь автором проекта
    if project.author == request.user:
        messages.error(request, 'Вы не можете подавать заявки на свои проекты')
        return redirect('project_detail', pk=project.id)

    # Проверяем, не подавал ли уже заявку
    existing_application = Application.objects.filter(
        project=project,
        applicant=request.user
    ).first()

    if existing_application:
        messages.error(request, 'Вы уже подавали заявку на этот проект')
        return redirect('project_detail', pk=project.id)

    if request.method == 'POST':
        # Создаем заявку
        application = Application.objects.create(
            project=project,
            applicant=request.user,
            message=request.POST.get('message', ''),
            applied_role_id=request.POST.get('role')
        )
        application._skip_notification = True
        if NOTIFICATIONS_ENABLED:
            try:
                notify_new_application(application)
                messages.info(request, 'Автор проекта уведомлен о вашей заявке')
            except Exception as e:
                print(f"Ошибка при отправке уведомления: {e}")
                # Не прерываем процесс из-за ошибки уведомлений

        messages.success(request, 'Заявка успешно подана!')
        return redirect('project_detail', pk=project.id)

    # GET запрос - показываем форму
    available_roles = project.needed_roles.all()
    context = {
        'project': project,
        'available_roles': available_roles,
    }
    return render(request, 'applications/create_application.html', context)


@login_required
def my_applications(request):
    """Заявки текущего пользователя"""
    applications = Application.objects.filter(applicant=request.user).order_by('-created_at')
    context = {
        'applications': applications,
        # Можно добавить дополнительные данные для уведомлений
    }

    # Если пользователь открыл страницу своих заявок,
    # можно пометить связанные уведомления как прочитанные
    if NOTIFICATIONS_ENABLED and applications.exists():
        try:
            from notifications.utils import mark_notifications_read_for_applications
            mark_notifications_read_for_applications(request.user, applications)
        except:
            pass  # Игнорируем ошибки в уведомлениях

    return render(request, 'applications/my_applications.html', context)


@login_required
def application_detail(request, pk):
    """Детальная страница заявки"""
    application = get_object_or_404(Application, pk=pk)

    # Проверяем, что пользователь имеет доступ к заявке
    if application.applicant != request.user and application.project.author != request.user:
        messages.error(request, 'Нет доступа к этой заявке')
        return redirect('projects_list')

    if NOTIFICATIONS_ENABLED:
        try:
            from notifications.models import Notification
            # Находим и помечаем уведомления, связанные с этой заявкой
            Notification.objects.filter(
                user=request.user,
                related_application=application,
                is_read=False
            ).update(is_read=True)
        except:
            pass  # Игнорируем ошибки в уведомлениях

    return render(request, 'applications/application_detail.html', {
        'application': application,
        'is_applicant': application.applicant == request.user,
        'is_project_author': application.project.author == request.user,
    })

@login_required
def process_application(request, pk, action):
    """Обработка заявки - принятие или отклонение"""
    application = get_object_or_404(Application, pk=pk)

    # Проверяем, что текущий пользователь - автор проекта
    if application.project.author != request.user:
        messages.error(request, 'Вы можете обрабатывать только заявки на свои проекты')
        return redirect('application_detail', pk=pk)

    # Проверяем, что действие допустимое
    if action not in ['accept', 'reject']:
        messages.error(request, 'Недопустимое действие')
        return redirect('application_detail', pk=pk)

    # Проверяем, что заявка еще не обработана
    if application.status != 'pending':
        messages.error(request, 'Эта заявка уже обработана')
        return redirect('application_detail', pk=pk)

    if request.method == 'POST':
        try:
            old_status = application.status

            if action == 'accept':
                application.status = 'accepted'
                status_display = 'принята'

                # Добавляем студента в команду проекта
                from projects.models import ProjectMember

                # Проверяем, не состоит ли уже студент в команде
                if not ProjectMember.objects.filter(
                        project=application.project,
                        user=application.applicant
                ).exists():

                    # Определяем роль для участника
                    role = application.applied_role
                    if not role:
                        # Если роль не указана в заявке, используем роль по умолчанию
                        from projects.models import ProjectRole
                        role, _ = ProjectRole.objects.get_or_create(
                            name='Участник',
                            defaults={'description': 'Участник проекта'}
                        )

                    # Добавляем в команду
                    ProjectMember.objects.create(
                        project=application.project,
                        user=application.applicant,
                        role=role
                    )

                    # Обновляем статус проекта если нужно
                    project = application.project
                    if project.status == 'active':
                        # Можно добавить логику изменения статуса проекта
                        pass

            elif action == 'reject':
                application.status = 'rejected'
                status_display = 'отклонена'

            application.save()

            # Отправляем уведомление студенту
            if NOTIFICATIONS_ENABLED and old_status != application.status:
                try:
                    notify_application_status(application, application.status)
                    messages.info(request, 'Студент уведомлен о решении')
                except Exception as e:
                    print(f"Ошибка при отправке уведомления: {e}")

            messages.success(request, f'Заявка успешно {status_display}!')

            # Редирект в зависимости от того, откуда пришли
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('project_applications', project_id=application.project.id)

        except Exception as e:
            print(f"Ошибка при обработке заявки: {e}")
            messages.error(request, f'Ошибка при обработке заявки: {str(e)}')
            return redirect('application_detail', pk=pk)

    # GET запрос - показываем страницу подтверждения
    return render(request, 'applications/process_application.html', {
        'application': application,
        'action': action,
        'action_display': 'принята' if action == 'accept' else 'отклонена'
    })


@login_required
def withdraw_application(request, pk):
    """Отзыв своей заявки студентом"""
    application = get_object_or_404(Application, pk=pk)

    # Проверяем, что текущий пользователь - автор заявки
    if application.applicant != request.user:
        messages.error(request, 'Вы можете отзывать только свои заявки')
        return redirect('application_detail', pk=pk)

    # Проверяем, что заявка еще не обработана
    if application.status != 'pending':
        messages.error(request, 'Нельзя отозвать уже обработанную заявку')
        return redirect('application_detail', pk=pk)

    if request.method == 'POST':
        # Сохраняем информацию для уведомления
        project_title = application.project.title
        project_author = application.project.author

        application.delete()

        # Уведомляем автора проекта об отзыве
        if NOTIFICATIONS_ENABLED:
            try:
                from notifications.utils import create_notification
                create_notification(
                    user=project_author,
                    notification_type='application_withdrawn',
                    message=f'Студент {request.user.get_full_name()} отозвал заявку на проект "{project_title}"',
                    project=application.project
                )
            except Exception as e:
                print(f"Ошибка при отправке уведомления об отзыве: {e}")

        messages.success(request, 'Заявка успешно отозвана!')
        return redirect('my_applications')

    return render(request, 'applications/withdraw_application.html', {
        'application': application
    })


@login_required
def project_applications(request, project_id):
    """Заявки на конкретный проект (для автора проекта)"""
    from projects.models import Project
    project = get_object_or_404(Project, pk=project_id)

    print(f"DEBUG: project_applications вызвана")
    print(f"DEBUG: project_id = {project_id}")
    print(f"DEBUG: project.title = {project.title}")
    print(f"DEBUG: project.author = {project.author.email}")
    print(f"DEBUG: request.user = {request.user.email}")

    # Проверяем, что пользователь - автор проекта
    if project.author != request.user:
        messages.error(request, 'Вы можете просматривать заявки только на свои проекты')
        return redirect('project_detail', pk=project.id)

    applications = Application.objects.filter(project=project).order_by('-created_at')

    print(f"DEBUG: Найдено заявок: {applications.count()}")
    for app in applications:
        print(f"DEBUG:   Заявка #{app.id} от {app.applicant.email}")

    # Статистика
    stats = {
        'total': applications.count(),
        'pending': applications.filter(status='pending').count(),
        'accepted': applications.filter(status='accepted').count(),
        'rejected': applications.filter(status='rejected').count(),
    }

    print(f"DEBUG: Статистика: {stats}")

    # Помечаем уведомления как прочитанные
    if NOTIFICATIONS_ENABLED and applications.exists():
        try:
            from notifications.models import Notification
            Notification.objects.filter(
                user=request.user,
                notification_type='new_application',
                related_project=project,
                is_read=False
            ).update(is_read=True)
        except:
            pass

    free_spaces_percent = 100 - int(
        (project.members.count / project.required_roles.count * 100)) if project.required_roles.count() > 0 else 0

    return render(request, 'applications/project_applications.html', {
        'project': project,
        'applications': applications,
        'stats': stats,
        'free_spaces_percent': free_spaces_percent,
    })
@login_required
def update_application_status(request, pk, status):
    """Обновление статуса заявки (принятие/отклонение)"""
    application = get_object_or_404(Application, pk=pk)

    # Проверяем, что пользователь - автор проекта
    if application.project.author != request.user:
        messages.error(request, 'Вы можете обновлять статус только заявок на свои проекты')
        return redirect('application_detail', pk=application.id)

    if status in ['accepted', 'rejected']:
        old_status = application.status
        application.status = status

        # Если принимаем заявку, добавляем студента в команду
        if status == 'accepted':
            from projects.models import ProjectMember, ProjectRole
            # Проверяем, не состоит ли уже студент в команде
            if not ProjectMember.objects.filter(
                    project=application.project,
                    user=application.applicant
            ).exists():
                # Получаем роль (если указана в заявке)
                role = None
                if application.applied_role_id:
                    try:
                        role = ProjectRole.objects.get(id=application.applied_role_id)
                    except ProjectRole.DoesNotExist:
                        # Создаем роль по умолчанию
                        role, _ = ProjectRole.objects.get_or_create(
                            name='Участник',
                            defaults={'description': 'Участник проекта'}
                        )
                else:
                    # Роль по умолчанию
                    role, _ = ProjectRole.objects.get_or_create(
                        name='Участник',
                        defaults={'description': 'Участник проекта'}
                    )

                # Добавляем в команду
                ProjectMember.objects.create(
                    project=application.project,
                    user=application.applicant,
                    role=role
                )

        application.save()


        if NOTIFICATIONS_ENABLED and old_status != status:
            try:
                notify_application_status(application, status)
                messages.info(request, 'Студент уведомлен о решении')
            except Exception as e:
                print(f"Ошибка при отправке уведомления о статусе: {e}")
                # Не прерываем процесс

        status_display = 'принята' if status == 'accepted' else 'отклонена'
        messages.success(request, f'Заявка {status_display}!')

    return redirect('project_applications', project_id=application.project.id)