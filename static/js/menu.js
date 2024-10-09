document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggle-sidebar');
    const sidebar = document.getElementById('sidebar');
    const contentWrapper = document.querySelector('.content-wrapper');

    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('show'); // Alterna a classe show
        if (sidebar.classList.contains('show')) {
            contentWrapper.style.marginLeft = '200px'; // Ajusta a margem quando a sidebar está visível
        } else {
            contentWrapper.style.marginLeft = '0'; // Remove a margem quando a sidebar está escondida
        }
    });
});
