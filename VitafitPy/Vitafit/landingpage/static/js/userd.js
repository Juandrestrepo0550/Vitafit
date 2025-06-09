 
        // Gráfico de progreso
        document.addEventListener('DOMContentLoaded', function() {
            const ctx = document.getElementById('progressChart').getContext('2d');
            const progressChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                    datasets: [
                        {
                            label: 'Minutos de ejercicio',
                            data: [30, 45, 35, 50, 40, 25, 60],
                            borderColor: '#10B981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            borderWidth: 3,
                            tension: 0.3,
                            fill: true
                        },
                        {
                            label: 'Calorías quemadas',
                            data: [250, 380, 300, 420, 350, 200, 500],
                            borderColor: '#3B82F6',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            borderWidth: 3,
                            tension: 0.3,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Mostrar/ocultar formulario de edición
            const editBtn = document.getElementById('editDataBtn');
            const cancelBtn = document.getElementById('cancelEditBtn');
            const updateForm = document.getElementById('updateForm');
            const userDataForm = document.getElementById('userDataForm');

            editBtn.addEventListener('click', function(e) {
                e.preventDefault();
                updateForm.classList.remove('hidden');
                updateForm.scrollIntoView({ behavior: 'smooth' });
            });

            cancelBtn.addEventListener('click', function() {
                updateForm.classList.add('hidden');
            });

            userDataForm.addEventListener('submit', function(e) {
                e.preventDefault();
                // Aquí iría la lógica para enviar los datos actualizados al servidor
                
                // Simulación de éxito
                alert('¡Tus datos se han actualizado correctamente!');
                updateForm.classList.add('hidden');
                
                // Actualizar los valores mostrados (en una implementación real, esto vendría del servidor)
                document.querySelectorAll('[data-user-data]').forEach(el => {
                    const field = el.getAttribute('data-user-data');
                    const newValue = document.getElementById(field).value;
                    el.textContent = newValue;
                });
            });

            // Notificación de bienvenida
            setTimeout(() => {
                const welcomeToast = document.createElement('div');
                welcomeToast.className = 'fixed bottom-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg flex items-center animate-fade-in-up';
                welcomeToast.innerHTML = `
                    <ion-icon name="checkmark-circle" class="text-xl mr-2"></ion-icon>
                    <span>¡Bienvenido de vuelta! Tu progreso va muy bien.</span>
                `;
                document.body.appendChild(welcomeToast);
                
                setTimeout(() => {
                    welcomeToast.classList.remove('animate-fade-in-up');
                    welcomeToast.classList.add('animate-fade-out-down');
                    setTimeout(() => welcomeToast.remove(), 500);
                }, 5000);
            }, 1000);
        });
