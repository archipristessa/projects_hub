// ===== REGISTRATION SCRIPT =====
// Обработка функционала страницы регистрации

/**
 * Выбор роли пользователя (студент/преподаватель)
 * @param {string} role - выбранная роль
 */
function selectRole(role) {
    // Снимаем выделение со всех вариантов
    document.querySelectorAll('.role-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // Выделяем выбранный вариант
    document.querySelector(`.role-option[onclick="selectRole('${role}')"]`).classList.add('selected');
    
    // Устанавливаем значение радиокнопки
    document.getElementById(role).checked = true;
}

/**
 * Валидация совпадения паролей
 * @returns {boolean} - результат проверки
 */
function validatePasswords() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const errorElement = document.getElementById('password-error');
    
    if (password !== confirmPassword) {
        errorElement.style.display = 'block';
        return false;
    } else {
        errorElement.style.display = 'none';
        return true;
    }
}

/**
 * Переход на главную страницу
 */
function goToMainPage() {
    window.location.href = 'index.html';
}

/**
 * Обработка отправки формы регистрации
 */
document.querySelector('.registration-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const lastname = document.getElementById('lastname').value;
    const firstname = document.getElementById('firstname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const role = document.querySelector('input[name="role"]:checked');
    
    // Проверка совпадения паролей
    if (!validatePasswords()) {
        alert('Пароли не совпадают!');
        return;
    }
    
    // Проверка заполнения обязательных полей
    if (!lastname || !firstname || !email || !password || !role) {
        alert('Пожалуйста, заполните все обязательные поля');
        return;
    }
    
    // Здесь будет код для отправки данных на сервер
    alert('Регистрация успешно отправлена!');
});

// Добавляем проверку паролей при вводе
document.getElementById('confirm-password').addEventListener('input', validatePasswords);
document.getElementById('password').addEventListener('input', validatePasswords);