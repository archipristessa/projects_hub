// ===== LOGIN SCRIPT =====
// Обработка функционала страницы входа

/**
 * Переход на главную страницу
 */
function goToMainPage() {
    window.location.href = 'index.html';
}

/**
 * Обработка отправки формы входа
 */
document.querySelector('.registration-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Валидация полей
    if (!email || !password) {
        alert('Пожалуйста, заполните все поля');
        return;
    }
    
    // Здесь будет код для отправки данных на сервер
    alert('Вход выполнен!');
});