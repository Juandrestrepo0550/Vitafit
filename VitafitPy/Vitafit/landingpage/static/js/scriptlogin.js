const btnSignIn = document.getElementById("sign-in"), //Creamos una variable sing-in
    btnSignUp = document.getElementById("sign-up"),//Creamos una variable sing-up
    containerFormRegister = document.querySelector(".register"),//Creamos una variable register que es container de registro
    containerFormLogin = document.querySelector(".login");//Creamos una variable login que es container de inicio de sesion

btnSignIn.addEventListener("click", e => {
    containerFormRegister.classList.add("hide"); // con la clase hide que esta en el css podremos mandar hacia arriba el formulario que se muestre en la pagina
    containerFormLogin.classList.remove("hide") // con esta linea removemos  la clase hide para que el formulario que esta en pagina empiece a salir y el formulario que estaba escondido empiece a bajar
}) //este pequeño bloque de codigo permite que cada que le demos click al boton de inicio de sesion, este se cambie con el formulario de registro


btnSignUp.addEventListener("click", e => {
    containerFormLogin.classList.add("hide");
    containerFormRegister.classList.remove("hide")
}) //este bloque de codigo es el mismo bloque que el de arriba pero la diferencia es que este bloque va dirigido hacia el formulario de registro

//Con este archivo de javascript vamos a añadir o quitar un formulario ademas que si nos fijamos en la clase hide que pusimos en el html nos daremos cuenta que cuando uno de los 2 formularios sube hace que el hide del html cambie al contenedor que este escondido, este cambio lo puedes ver desde la consola del navegador que estes usando


document.addEventListener("DOMContentLoaded", function () {
    const signUpBtn = document.getElementById("sign-up");
    const signInBtn = document.getElementById("sign-in");

    const loginContainer = document.querySelector(".container-form.login");
    const registerContainer = document.querySelector(".container-form.register");

    const loginForm = document.querySelector(".form-login");
    const registerForm = document.querySelector(".form-register");

    function limpiarFormulario(formulario) {
        formulario.reset(); // Limpia los inputs
        const mensajes = formulario.querySelectorAll(".alert");
        mensajes.forEach(msg => msg.remove()); // Borra los mensajes
    }

    if (signUpBtn) {
        signUpBtn.addEventListener("click", function () {
            loginContainer.classList.add("hide");
            registerContainer.classList.remove("hide");
            limpiarFormulario(loginForm);
        });
    }

    if (signInBtn) {
        signInBtn.addEventListener("click", function () {
            registerContainer.classList.add("hide");
            loginContainer.classList.remove("hide");
            limpiarFormulario(registerForm);
        });
    }
});

// Validación de formularios

document.getElementById("correo").addEventListener("blur", function() {
    const correo = this.value.trim();
    const errorSpan = document.getElementById("correo-error");
    if (correo === "") {
        errorSpan.textContent = "";
        return;
    }

    fetch('/app.com/val_correo/?correo=' + encodeURIComponent(correo))
    .then(response => response.json())
    .then(data => {
        if (data.existe) {
            errorSpan.textContent = "Este correo ya está registrado.";
        } else {
            errorSpan.textContent = "";
        }
    })
    .catch(() => {
        errorSpan.textContent = "Error al validar el correo.";
    });
});

