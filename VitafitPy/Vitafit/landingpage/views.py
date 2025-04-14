from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone
from .models import Usuarios
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        nickname = request.POST.get('nickname', '').strip()
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '')
        repetircontrasena = request.POST.get('repetircontrasena', '')

        # Separar el nombre completo en nombres y apellidos
        partes = nombre_completo.split()
        nombres = partes[0] if len(partes) > 0 else ''
        apellidos = ' '.join(partes[1:]) if len(partes) > 1 else ''

        # Validar que todos los campos estén completos antes de continuar
        if not nombre_completo or not nickname or not correo or not contrasena or not repetircontrasena:
            messages.error(request, "Por favor completa todos los campos.")
            return render(request, 'login.html')

        # Verificar que las contraseñas coincidan
        if contrasena != repetircontrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'login.html')

        # Crear el nuevo usuario
        usuario = Usuarios(
            nombres=nombres,
            apellidos=apellidos,
            nickname=nickname,
            correo=correo,
            contrasena=make_password(contrasena),
            fecha_registro=timezone.now(),
            fecha_modificacion=timezone.now(),
            estado='activo',
            rol='usuario'
        )
        usuario.save()
        messages.success(request, "Usuario registrado correctamente.")
        return redirect('login')

    return render(request, 'Vitafit/landingpage/login.html')

def inicio_sesion(request):
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '').strip()

        # Validar campos vacíos
        if not correo or not contrasena:
            messages.error(request, "Por favor ingresa correo y contraseña.")
            return render(request, 'login.html')
        
        try:
            usuario = Usuarios.objects.get(correo=correo)
        except Usuarios.DoesNotExist:
            messages.error(request, "El correo no está registrado.")
            return render(request, 'login.html')
        
        
        # Validar contraseña
        if check_password(contrasena, usuario.contrasena):
            # Guardar datos en sesión si quieres (opcional)
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nickname
            messages.success(request, f"¡Bienvenido {usuario.nickname}!")
            return redirect('index')  # Redirige a la página principal o dashboard
        else:
            messages.error(request, "Contraseña incorrecta.")
            return render(request, 'login.html')
        
        return render(request, 'login.html')
