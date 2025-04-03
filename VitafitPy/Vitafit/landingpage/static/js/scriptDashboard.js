const hamBurger = document.querySelector("#toggle-btn"); 

hamBurger.addEventListener("click", function () {
    const sidebar = document.querySelector("#sidebar");
    sidebar.classList.toggle("expand");

    // Mostrar los submenús si el sidebar está colapsado
    if (!sidebar.classList.contains("expand")) {
        const dropdowns = document.querySelectorAll('.sidebar-item .sidebar-dropdown');
        dropdowns.forEach(dropdown => {
            dropdown.style.display = 'none'; // Colapsar todos los submenús
        });
    }
});

// Controlar los submenús al hacer clic
const sidebarLinks = document.querySelectorAll('.sidebar-link[data-bs-toggle="collapse"]');
sidebarLinks.forEach(link => {
    link.addEventListener('click', function () {
        if (!document.querySelector("#sidebar").classList.contains('expand')) {
            const dropdown = this.nextElementSibling;
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        }
    });
});

document.querySelector('form').addEventListener('submit', function() {
    var myModal = new bootstrap.Modal(document.getElementById('exampleModal'));
    myModal.hide(); // Cierra el modal después de enviar el formulario
});

