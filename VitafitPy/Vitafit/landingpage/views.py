from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Usuarios
import json
import openai

# Páginas básicas
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

# Registro de usuario
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
            contrasena=make_password(contrasena),
            rol='user',
            estado='activo',
            fecha_registro=timezone.now(),
            fecha_modificacion=timezone.now()
        )
        usuario.save()

        messages.success(request, "Usuario registrado correctamente.")
        return redirect(f"{reverse('login')}?registro=ok")

    return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'register'})

# Validar correo (AJAX)
def val_correo(request):
    correo = request.GET.get('correo', '').strip()
    existe = Usuarios.objects.filter(correo=correo).exists()
    return JsonResponse({'existe': existe})

# Inicio de sesión
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
            request.session['usuario_nombre'] = usuario.nombres  # O usar nickname si prefieres
            request.session['rol'] = usuario.rol

            messages.success(request, f"¡Bienvenido {usuario.nombres}!")
            return redirect('index')
        else:
            messages.error(request, "Contraseña incorrecta.")
            return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'login'})

    return render(request, 'Vitafit/landingpage/login.html', {'form_type': 'login'})

# Cerrar sesión
def cerrar_sesion(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('index')

# Vistas protegidas
@login_required(login_url='login')
def rutines(request):
    return render(request, 'rutinas.html')

@login_required(login_url='login')
def userd(request):
    return render(request, 'user.html')

def adminpage(request):
    return render(request, 'dashboard.html')

def recomendaciones_vi(request):
    return render(request, 'recomendaciones.html')

# Chat con OpenAI (recomendaciones)
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje_usuario = data.get("mensaje")

            if not mensaje_usuario:
                return JsonResponse({"error": "Falta el mensaje."}, status=400)

            openai.api_key = settings.OPENAI_API_KEY

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en salud, ejercicios y nutrición. Solo da recomendaciones dentro de estos temas. Sé claro, breve, y no des consejos médicos profesionales. Si alguien pregunta algo fuera de estos temas, indica que solo puedes hablar de salud y fitness."
                    },
                    {
                        "role": "user",
                        "content": mensaje_usuario
                    }
                ]
            )

            respuesta_ai = response.choices[0].message["content"]
            return JsonResponse({"respuesta": respuesta_ai})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
