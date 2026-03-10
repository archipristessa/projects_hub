from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User, ProfileStudent, ProfileTeacher
from .forms import ProfileStudentForm, ProfileTeacherForm


# HTML views
@login_required
def profile_view(request):
    """Просмотр профиля"""
    context = {}

    if request.user.user_type == 'student' and hasattr(request.user, 'student_profile'):
        context['profile'] = request.user.student_profile
    elif request.user.user_type == 'teacher' and hasattr(request.user, 'teacher_profile'):
        context['profile'] = request.user.teacher_profile

    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request):
    """Редактирование профиля"""
    try:
        if request.user.user_type == 'student':
            # Пытаемся найти существующий профиль
            try:
                profile = ProfileStudent.objects.get(user=request.user)
            except ProfileStudent.DoesNotExist:
                # Если профиля нет, создаем его
                profile = ProfileStudent.objects.create(
                    user=request.user,
                    institute='',
                    course=1,
                    group='',
                    skills='',
                    bio='',
                    phone='',
                    telegram='',
                    github='',
                    portfolio=''
                )

            form_class = ProfileStudentForm
            template = 'edit_profile_student.html'

        elif request.user.user_type == 'teacher':
            try:
                profile = ProfileTeacher.objects.get(user=request.user)
            except ProfileTeacher.DoesNotExist:
                profile = ProfileTeacher.objects.create(
                    user=request.user,
                    department='',
                    position='',
                    academic_degree='',
                    expertise='',
                    bio='',
                    phone='',
                    office=''
                )

            form_class = ProfileTeacherForm
            template = 'edit_profile_teacher.html'

        else:
            messages.error(request, 'Неизвестный тип пользователя')
            return redirect('profile')

        if request.method == 'POST':
            form = form_class(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('profile')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        else:
            form = form_class(instance=profile)

        return render(request, template, {'form': form})

    except Exception as e:
        messages.error(request, f'Ошибка при загрузке формы: {str(e)}')
        return redirect('profile')

def register_view(request):
    if request.method == 'POST':
        try:
            # Проверяем обязательные поля
            required_fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'user_type']
            for field in required_fields:
                if not request.POST.get(field):
                    messages.error(request, f'Поле {field} обязательно для заполнения!')
                    return render(request, 'registration/register.html')

            # Проверяем совпадение паролей
            if request.POST['password1'] != request.POST['password2']:
                messages.error(request, 'Пароли не совпадают!')
                return render(request, 'registration/register.html')

            # Проверяем длину пароля
            if len(request.POST['password1']) < 8:
                messages.error(request, 'Пароль должен содержать минимум 8 символов!')
                return render(request, 'registration/register.html')

            # Проверяем, что email не занят
            if User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, 'Пользователь с таким email уже существует!')
                return render(request, 'registration/register.html')

            # Проверяем корректность типа пользователя
            valid_user_types = ['student', 'teacher']
            if request.POST['user_type'] not in valid_user_types:
                messages.error(request, 'Неверный тип пользователя!')
                return render(request, 'registration/register.html')

            # Создаем пользователя
            user = User.objects.create_user(
                username=request.POST['email'],  # Используем email как username
                email=request.POST['email'],
                password=request.POST['password1'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                patronymic=request.POST.get('patronymic', ''),
                user_type=request.POST['user_type']
            )

            # Создаем профиль
            if user.user_type == 'student':
                ProfileStudent.objects.create(
                    user=user,
                    institute=request.POST.get('institute', ''),
                    course=request.POST.get('course'),  # Может быть None
                    group=request.POST.get('group', ''),
                    skills=request.POST.get('skills', ''),
                    bio=request.POST.get('bio', '')
                )
                messages.success(request, 'Регистрация студента прошла успешно! Заполните профиль в личном кабинете.')
            elif user.user_type == 'teacher':
                ProfileTeacher.objects.create(
                    user=user,
                    department=request.POST.get('department', ''),
                    position=request.POST.get('position', ''),
                    academic_degree=request.POST.get('academic_degree', ''),
                    expertise=request.POST.get('expertise', ''),
                    bio=request.POST.get('bio', '')
                )
                messages.success(request, 'Регистрация преподавателя прошла успешно! Заполните профиль в личном кабинете.')

            # Автоматически логиним пользователя
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name}!')
            return redirect('profile')

        except Exception as e:
            messages.error(request, f'Ошибка регистрации: {str(e)}')
            return render(request, 'registration/register.html')

    # GET запрос - просто показываем форму
    return render(request, 'registration/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.first_name}!")
            return redirect('profile')
        else:
            messages.error(request, "Неверный email или пароль.")

    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

