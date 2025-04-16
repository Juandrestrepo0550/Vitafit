from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone
from .models import Usuarios
from django.contrib.auth.hashers import check_password
from django.urls import reverse


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

        partes = nombre_completo.split()
        nombres = partes[0] if len(partes) > 0 else ''
        apellidos = ' '.join(partes[1:]) if len(partes) > 1 else ''

        if not nombre_completo or not nickname or not correo or not contrasena or not repetircontrasena:
            messages.error(request, "Por favor completa todos los campos.")
            return render(request, 'login.html', {'form_type': 'register'})

        if contrasena != repetircontrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'login.html', {'form_type': 'register'})

        # Validar si el correo ya está registrado
        if Usuarios.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return render(request, 'login.html', {'form_type': 'register'})

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
        return redirect(f"{reverse('inicio_sesion')}?registro=ok")

    return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'register'})

def inicio_sesion(request):
    correo = request.POST.get('correo', '').strip()
    contrasena = request.POST.get('contrasena', '').strip()

    if not correo or not contrasena:
        messages.error(request, "Por favor ingresa correo y contraseña.")
        return render(request, 'login.html', {'form_type': 'login'})

    usuarios = Usuarios.objects.filter(correo=correo)

    if not usuarios.exists():
        messages.error(request, "El correo no está registrado.")
        return render(request, 'login.html', {'form_type': 'login'})

    usuario = usuarios.first()

    if check_password(contrasena, usuario.contrasena):
        request.session['usuario_id'] = usuario.id
        request.session['usuario_nombre'] = usuario.nickname
        messages.success(request, f"¡Bienvenido {usuario.nickname}!")
        return redirect('index')
    else:
        messages.error(request, "Contraseña incorrecta.")
        return render(request, 'login.html', {'form_type': 'login'})

    return render(request, 'Vitafit/landingpage/login.html')


def cerrar_sesion(request):
    request.session.flush()  # Borra toda la sesión
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('index')

def adminpage(request):
    return render(request, 'dashboard.html')


