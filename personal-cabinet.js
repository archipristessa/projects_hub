// ===== PERSONAL CABINET SCRIPTS =====

// Функция переключения вкладок
function showTab(tabName) {
    // Скрыть все вкладки
    document.querySelectorAll('.tab-pane').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Показать выбранную вкладку
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Обновить активную кнопку вкладки
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Обновить активную ссылку в боковой панели
    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.classList.remove('active');
        if (link.textContent.includes(getTabTitle(tabName))) {
            link.classList.add('active');
        }
    });
}

// Вспомогательная функция для получения заголовка вкладки
function getTabTitle(tabName) {
    const titles = {
        'profile': 'Мой профиль',
        'projects': 'Мои проекты',
        'applications': 'Мои заявки',
        'team': 'Моя команда'
    };
    return titles[tabName] || '';
}

// Функция добавления навыка
function addSkill() {
    const skill = prompt('Введите новый навык:');
    if (skill && skill.trim()) {
        const skillsContainer = document.querySelector('.skills-container');
        const skillTag = document.createElement('div');
        skillTag.className = 'skill-tag';
        skillTag.textContent = skill.trim();
        
        // Вставить перед кнопкой добавления
        const addButton = document.querySelector('.add-skill-btn');
        skillsContainer.insertBefore(skillTag, addButton);
        
        alert(`Навык "${skill.trim()}" добавлен!`);
    }
}

// Функция редактирования профиля
function editProfile() {
    alert('Редактирование профиля. Здесь будет форма редактирования.');
    // В реальном приложении здесь будет открытие модального окна или переход на страницу редактирования
}

// Функция создания проекта
function createProject() {
    alert('Создание нового проекта. Здесь будет форма создания проекта.');
    // В реальном приложении здесь будет открытие формы создания проекта
}

// Функция выхода из аккаунта
function logout() {
    if (confirm('Вы уверены, что хотите выйти?')) {
        window.location.href = 'index.html';
    }
}

// Инициализация вкладок при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Назначаем обработчики для кнопок вкладок
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            showTab(this.dataset.tab);
        });
    });
    
    // Инициализируем первую вкладку как активную
    showTab('profile');
});