document.querySelector('.registration-form').addEventListener('submit', function() {
    const btn = this.querySelector('.btn');
    btn.textContent = 'Вход...';
    btn.disabled = true;
});