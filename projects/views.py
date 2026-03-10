from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Project, ProjectMember, ProjectRole


def home_page(request):
    """Главная страница с лентой последних проектов"""
    # Берем последние 6 проектов для ленты
    latest_projects = Project.objects.all().order_by('-created_at')[:6]

    context = {
        'latest_projects': latest_projects,
    }
    return render(request, 'home.html', context)
@login_required
def projects_list(request):
    """Список всех проектов"""
    projects = Project.objects.all().order_by('-created_at')

    # Поиск проектов
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(requirements__icontains=search_query)
        )

    # Фильтрация по статусу
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)

    context = {
        'projects': projects,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'projects/list.html', context)


@login_required
def project_detail(request, pk):
    """Детальная страница проекта"""
    project = get_object_or_404(Project, pk=pk)

    # Проверяем, подавал ли пользователь заявку на этот проект
    user_application = None
    if hasattr(request.user, 'applications'):
        user_application = request.user.applications.filter(project=project).first()

    context = {
        'project': project,
        'user_application': user_application,
        'is_author': project.author == request.user,
    }
    return render(request, 'projects/detail.html', context)


@login_required
def create_project(request):
    """Создание нового проекта"""
    if request.method == 'POST':
        try:
            # Проверяем обязательные поля
            if not request.POST.get('title'):
                messages.error(request, 'Название проекта обязательно!')
                return render(request, 'projects/create_project.html')

            if not request.POST.get('description'):
                messages.error(request, 'Описание проекта обязательно!')
                return render(request, 'projects/create_project.html')

            # Создаем проект
            project = Project.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                requirements=request.POST.get('requirements', ''),
                status=request.POST.get('status', 'active'),
                author=request.user
            )

            # Добавляем нужные роли
            roles_ids = request.POST.getlist('needed_roles')
            if roles_ids:
                roles = ProjectRole.objects.filter(id__in=roles_ids)
                project.needed_roles.set(roles)

            messages.success(request, 'Проект успешно создан!')
            return redirect('project_detail', pk=project.id)

        except Exception as e:
            messages.error(request, f'Ошибка при создании проекта: {str(e)}')
            return render(request, 'projects/create_project.html')

    # GET запрос - показываем форму
    roles = ProjectRole.objects.all()
    return render(request, 'projects/create_project.html', {'roles': roles})


@login_required
def edit_project(request, pk):
    """Редактирование проекта"""
    project = get_object_or_404(Project, pk=pk)

    # Проверяем, что пользователь - автор проекта
    if project.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои проекты')
        return redirect('project_detail', pk=project.id)

    if request.method == 'POST':
        try:
            # Проверяем обязательные поля
            if not request.POST.get('title'):
                messages.error(request, 'Название проекта обязательно!')
                return redirect('edit_project', pk=project.id)

            if not request.POST.get('description'):
                messages.error(request, 'Описание проекта обязательно!')
                return redirect('edit_project', pk=project.id)

            # Обновляем проект
            project.title = request.POST.get('title')
            project.description = request.POST.get('description')
            project.requirements = request.POST.get('requirements', '')
            project.status = request.POST.get('status', 'active')
            project.save()

            # Обновляем роли
            roles_ids = request.POST.getlist('needed_roles')
            roles = ProjectRole.objects.filter(id__in=roles_ids)
            project.needed_roles.set(roles)

            messages.success(request, 'Проект успешно обновлен!')
            return redirect('project_detail', pk=project.id)

        except Exception as e:
            messages.error(request, f'Ошибка при обновлении проекта: {str(e)}')

    # GET запрос - показываем форму с текущими данными
    roles = ProjectRole.objects.all()
    context = {
        'project': project,
        'roles': roles,
    }
    return render(request, 'projects/edit_project.html', context)


@login_required
def delete_project(request, pk):
    """Удаление проекта"""
    project = get_object_or_404(Project, pk=pk)

    if project.author != request.user:
        messages.error(request, 'Вы можете удалять только свои проекты')
        return redirect('project_detail', pk=project.id)

    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'Проект "{project_title}" успешно удален!')
        return redirect('projects_list')

    return render(request, 'projects/delete_project.html', {'project': project})


# projects/views.py
@login_required
def my_projects(request):
    """Проекты текущего пользователя"""
    # Проекты, где пользователь автор
    projects = Project.objects.filter(author=request.user).order_by('-created_at')
    projects = projects.prefetch_related('applications', 'members', 'required_roles')

    # Добавляем аннотации для подсчета заявок
    from django.db.models import Count, Q
    projects = projects.annotate(
        total_applications=Count('applications'),
        pending_applications=Count('applications', filter=Q(applications__status='pending'))
    )
    # Фильтрация по статусу
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)

    # Поиск по названию
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(title__icontains=search_query)

    # Статистика
    active_count = Project.objects.filter(author=request.user, status='active').count()
    completed_count = Project.objects.filter(author=request.user, status='completed').count()
    archived_count = Project.objects.filter(author=request.user, status='archived').count()

    # Проекты, где пользователь участник (не автор)
    from projects.models import ProjectMember
    user_participation_projects = ProjectMember.objects.filter(
        user=request.user
    ).exclude(project__author=request.user).select_related('project', 'role')

    # Пагинация (если нужно)
    # from django.core.paginator import Paginator
    # paginator = Paginator(projects, 6)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {
        'projects': projects,
        # 'page_obj': page_obj,
        # 'is_paginated': paginator.num_pages > 1,
        'active_count': active_count,
        'completed_count': completed_count,
        'archived_count': archived_count,
        'user_participation_projects': user_participation_projects,
    }

    return render(request, 'projects/my_projects.html', context)


def project_roles_list(request):
    """Список ролей в проектах (для выпадающих списков)"""
    roles = ProjectRole.objects.all()
    return render(request, 'projects/roles_list.html', {'roles': roles})


@login_required
def apply_to_project(request, pk):
    """Подача заявки на участие в проекте"""
    project = get_object_or_404(Project, pk=pk)

    # Проверяем, что пользователь не автор проекта
    if project.author == request.user:
        messages.error(request, 'Вы не можете подать заявку на свой собственный проект')
        return redirect('project_detail', pk=project.pk)

    # Проверяем, не подал ли уже заявку
    from applications.models import Application  # ← Импортируем модель
    existing_application = Application.objects.filter(
        project=project,
        applicant=request.user
    ).first()

    if existing_application:
        messages.warning(request, 'Вы уже подали заявку на этот проект')
        return redirect('project_detail', pk=project.pk)

    if request.method == 'POST':
        try:
            # Создаем заявку
            application = Application.objects.create(
                project=project,
                applicant=request.user,
                message=request.POST.get('message', ''),
                status='pending'  # Статус по умолчанию
            )

            # Уведомляем автора проекта
            try:
                from notifications.utils import notify_new_application
                notify_new_application(application)
                messages.info(request, 'Автор проекта уведомлен о вашей заявке')
            except Exception as e:
                print(f"Ошибка при отправке уведомления: {e}")
                # Не прерываем процесс из-за ошибки уведомлений

            messages.success(request, f'Заявка на проект "{project.title}" успешно подана!')
            return redirect('project_detail', pk=project.pk)

        except Exception as e:
            messages.error(request, f'Ошибка при подаче заявки: {str(e)}')
            return redirect('project_detail', pk=project.pk)

    # Если GET запрос, показываем форму подачи заявки
    context = {
        'project': project,
    }
    return render(request, 'projects/apply_to_project.html', context)