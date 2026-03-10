// ===== REGISTRATION SCRIPT =====
// Минимальный JS для улучшения UX формы регистрации

/**
 * Выбор роли пользователя (студент/преподаватель)
 */
function selectRole(role) {
    // Устанавливаем значение скрытого поля
    document.querySelector('input[name="user_type"][value="' + role + '"]').checked = true;

    // Визуальное выделение выбранной роли
    document.querySelectorAll('.role-option').forEach(option => {
        option.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
}

/**
 * Проверка совпадения паролей при вводе
 */
function setupPasswordValidation() {
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');

    if (password1 && password2) {
        password2.addEventListener('input', function() {
            if (password1.value !== password2.value) {
                password2.style.borderColor = '#ff4444';
            } else {
                password2.style.borderColor = '#00C781';
            }
        });
    }
}

/**
 * Показ/скрытие дополнительных полей в зависимости от роли
 */
function setupRoleDependentFields() {
    const roleOptions = document.querySelectorAll('input[name="user_type"]');

    roleOptions.forEach(radio => {
        radio.addEventListener('change', function() {
            // Можно добавить логику показа разных полей для студента/преподавателя
            console.log('Выбрана роль:', this.value);
        });
    });
}

/**
 * Индикация загрузки при отправке формы
 */
function setupLoadingState() {
    const form = document.querySelector('.registration-form');

    form.addEventListener('submit', function() {
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        // Меняем текст кнопки на время отправки
        submitBtn.textContent = 'Регистрация...';
        submitBtn.disabled = true;

        // Восстанавливаем через 5 секунд на случай ошибки
        setTimeout(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 5000);
    });
}

/**
 * Быстрая валидация email перед отправкой
 */
function validateEmail(email) {
    return email.includes('@') && email.includes('.');
}

/**
 * Основная инициализация
 */
document.addEventListener('DOMContentLoaded', function() {
    setupPasswordValidation();
    setupRoleDependentFields();
    setupLoadingState();

    // Простая проверка формы перед отправкой (не блокирующая)
    const form = document.querySelector('.registration-form');
    form.addEventListener('submit', function(e) {
        const email = document.getElementById('email');
        const password1 = document.getElementById('password1');
        const password2 = document.getElementById('password2');

        // Быстрая проверка email
        if (email && !validateEmail(email.value)) {
            email.style.borderColor = '#ff4444';
            // Не preventDefault() - пусть Django сам проверит
        }

        // Проверка паролей
        if (password1 && password2 && password1.value !== password2.value) {
            // Просто подсвечиваем, но не блокируем отправку
            password2.style.borderColor = '#ff4444';
        }
    });
});

/**
 * Переход на главную страницу
 */
function goToMainPage() {
    window.location.href = '/';
}