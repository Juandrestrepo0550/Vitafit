from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from .models import Usuarios
from django.contrib import messages
from django.utils import timezone

# Create your views here.


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        nickname = request.POST('nicknames')
        correo = request.POST('correos')
        contrasena = request.POST('contrasenas')
        repetircontrasena = request.POST('repetircontrasenas')

        # Verificar que las contraseñas coincidan
        if contrasena != repetircontrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'Vitafit/landingpage/login.html')

        # Crear el nuevo usuario
        usuario = Usuarios(
            nicknames=nickname,
            correos=correo,
            contrasenas=make_password(contrasena),  # Hashea la contraseña
            fecha_registro=timezone.now(),
            fecha_modificacion=timezone.now(),
            estado='activo',  # Puedes personalizar este valor
            rol='usuario' 
        )
        usuario.save()
        messages.success(request, "Usuario registrado correctamente.")
        return redirect('login')  # Redirige a donde lo necesites después del registro

    return render(request, 'Vitafit/landingpage/login.html')