from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Ejercicio, Rutina, RutinaEjercicio
from .forms import EjercicioForm, RutinaForm
from .models import Usuarios
from .models import Usuarios, HistorialPersonalUsuario
import json
import openai
from datetime import datetime

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

# @login_required(login_url='login')
# def userd(request):
#     return render(request, 'user.html')

@login_required(login_url='login')
def userd(request):
    # Obtener el usuario autenticado
    usuario = None
    if 'usuario_id' in request.session:
        try:
            usuario = Usuarios.objects.get(id=request.session['usuario_id'])
        except Usuarios.DoesNotExist:
            messages.error(request, "Usuario no encontrado en la tabla usuarios.")
            return redirect('login')
    else:
        # Si el usuario está autenticado vía auth_user (e.g., Google login)
        try:
            usuario = Usuarios.objects.get(correo=request.user.email)
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombres
            request.session['rol'] = usuario.rol
        except Usuarios.DoesNotExist:
            messages.error(request, "No tienes un perfil en VitaFIT. Por favor, registra un perfil.")
            return redirect('register')

    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else request.POST
            altura = data.get('altura')
            peso = data.get('peso')
            edad = data.get('edad')
            objetivo = data.get('objetivo')

            # Validar inputs
            if not all([altura, peso, edad, objetivo]):
                return JsonResponse({'error': 'Todos los campos son obligatorios.'}, status=400)

            try:
                altura = float(altura)
                peso = float(peso)
                edad = int(edad)
                if altura <= 0 or peso <= 0:
                    return JsonResponse({'error': 'Altura y peso deben ser mayores a 0.'}, status=400)
                if edad < 0 or edad > 150:
                    return JsonResponse({'error': 'La edad debe estar entre 0 y 150 años.'}, status=400)
            except ValueError:
                return JsonResponse({'error': 'Altura, peso y edad deben ser números válidos.'}, status=400)

            valid_objetivos = [choice[0] for choice in Usuarios.objetivo.field.choices]
            if objetivo not in valid_objetivos:
                return JsonResponse({'error': 'Objetivo inválido.'}, status=400)

            # Guardar historial de peso y altura
            if usuario.peso != peso or usuario.altura != altura: HistorialPersonalUsuario.objects.create(
                    usuario=usuario,
                    peso_anterior=usuario.peso,
                    altura_anterior=usuario.altura
                )

            # Actualizar datos
            usuario.altura = altura
            usuario.peso = peso
            usuario.Edad = edad
            usuario.objetivo = objetivo
            usuario.fecha_modificacion = timezone.now()
            usuario.save()

            # Calcular IMC
            imc = round(peso / ((altura / 100) ** 2), 2)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': 'Datos actualizados correctamente.',
                    'usuario': {
                        'nombre': f"{usuario.nombres} {usuario.apellidos}",
                        'altura': usuario.altura,
                        'peso': usuario.peso,
                        'edad': usuario.Edad,
                        'objetivo': usuario.objetivo,
                        'imc': imc
                    }
                })
            else:
                messages.success(request, 'Datos actualizados correctamente.')
                return redirect('userd')

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': str(e)}, status=500)
            else:
                messages.error(request, f'Error al actualizar: {str(e)}')
                return redirect('userd')

    # Calcular IMC para el contexto
    imc = round(usuario.peso / ((usuario.altura / 100) ** 2), 2) if usuario.altura and usuario.peso else None

    context = {
        'usuario': usuario,
        'imc': imc
    }
    return render(request, 'user.html', context)

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

#crear ejercicios
def crear_ejercicio_ajax(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            ejercicio = form.save()
            return JsonResponse({
                'success': True,
                'ejercicio': {
                    'id': ejercicio.id,
                    'nombre': ejercicio.nombre,
                }
            })
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

#crear rutinas
def crear_rutina(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        ejercicios_ids = request.POST.getlist('ejercicios')  # checkbox con name="ejercicios"
        if form.is_valid():
            rutina = form.save()
            for idx, eid in enumerate(ejercicios_ids):
                ejercicio = get_object_or_404(Ejercicio, pk=eid)
                RutinaEjercicio.objects.create(
                    rutina=rutina,
                    ejercicio=ejercicio,
                    orden=idx,
                    cantidad_ejercicios=1  # o extraes otro input si lo defines
                )
            return redirect('detalle_rutina', pk=rutina.pk)
    else:
        form = RutinaForm()
    ejercicios = Ejercicio.objects.all()
    return render(request, 'crear_rutina.html', {
        'form': form,
        'ejercicios': ejercicios,
    })