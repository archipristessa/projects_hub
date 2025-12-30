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

function goToMainPage() {
    // Заглушка - переход на главную страницу
    alert('Переход на главную страницу');
    // window.location.href = 'index.html'; // Раскомментировать когда будет готова главная страница
}

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