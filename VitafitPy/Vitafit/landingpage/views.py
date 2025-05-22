from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone
from .models import Usuarios
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '')
        repetircontrasena = request.POST.get('repetircontrasena', '')

        if not nombres or not apellidos or not correo or not contrasena or not repetircontrasena:
            messages.error(request, "Por favor completa todos los campos.")
            return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'register'})

        if contrasena != repetircontrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'register'})

        usuario = Usuarios(
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            contrasena=make_password(contrasena),  # Hashea la contraseña
            rol='user',  # Valor por defecto según tu tabla
            estado='activo',
            fecha_registro=timezone.now(),
            fecha_modificacion=timezone.now()
        )
        usuario.save()

        messages.success(request, "Usuario registrado correctamente.")
        return redirect(f"{reverse('login')}?registro=ok")

    return render(request, 'login.html', {'form_type': 'register'})

def val_correo(request):
    correo = request.GET.get('correo', '').strip()
    existe = Usuarios.objects.filter(correo=correo).exists()
    return JsonResponse({'existe': existe})

def inicio_sesion(request):
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '').strip()

        if not correo or not contrasena:
            messages.error(request, "Por favor ingresa correo y contraseña.")
            return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'login'})

        usuarios = Usuarios.objects.filter(correo=correo)

        if not usuarios.exists():
            messages.error(request, "El correo no está registrado.")
            return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'login'})

        usuario = usuarios.first()

        if check_password(contrasena, usuario.contrasena):
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombres  # Puedes concatenar con apellidos si prefieres
            request.session['rol'] = usuario.rol  # Importante para mostrar botones por rol

            messages.success(request, f"¡Bienvenido {usuario.nombres}!")
            return redirect('index')
        else:
            messages.error(request, "Contraseña incorrecta.")
            return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'login'})

    # Si no es POST, simplemente renderiza el login
    return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'login'})


def cerrar_sesion(request):
    request.session.flush()  # Borra toda la sesión
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('index')

def adminpage(request):
    return render(request, 'dashboard.html')

def rutines(request):
    return render(request, 'rutinas.html')


