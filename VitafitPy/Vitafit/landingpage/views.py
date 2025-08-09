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
from .models import DatosUsuario
from .models import Usuarios, HistorialPersonalUsuario
import json
import openai
from datetime import datetime, date
from django.http import JsonResponse



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
            return render(request, "socialaccount/login.html", {'form_type': 'register'})

        if contrasena != repetircontrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "socialaccount/login.html", {'form_type': 'register'})

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

    return render(request, 'socialaccount/login.html', {'form_type': 'register'})

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
            return render(request, 'socialaccount/login.html', {'form_type': 'login'})

        usuarios = Usuarios.objects.filter(correo=correo)

        if not usuarios.exists():
            messages.error(request, "El correo no está registrado.")
            return render(request, 'socialaccount/login.html', {'form_type': 'login'})

        usuario = usuarios.first()

        if check_password(contrasena, usuario.contrasena):
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombres  # O usar nickname si prefieres
            request.session['rol'] = usuario.rol

            messages.success(request, f"¡Bienvenido {usuario.nombres}!")
            return redirect('index')
        else:
            messages.error(request, "Contraseña incorrecta.")
            return render(request, 'socialaccount/login.html', {'form_type': 'login'})

    return render(request, 'socialaccount/login.html', {'form_type': 'login'})

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
    # Obtener usuario autenticado
    usuario = None
    if 'usuario_id' in request.session:
        try:
            usuario = Usuarios.objects.get(id=request.session['usuario_id'])
        except Usuarios.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Usuario no encontrado en la tabla usuarios.'}, status=404)
            messages.error(request, "Usuario no encontrado en la tabla usuarios.")
            return redirect('login')
    else:
        try:
            usuario = Usuarios.objects.get(correo=request.user.email)
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombres
            request.session['rol'] = usuario.rol
        except Usuarios.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'No tienes un perfil en VitaFIT. Por favor, registra un perfil.'}, status=404)
            messages.error(request, "No tienes un perfil en VitaFIT. Por favor, registra un perfil.")
            return redirect('register')

    # Obtener o crear datos del usuario
    datos_usuario, _ = DatosUsuario.objects.get_or_create(id_usuario=usuario)

    if request.method == 'POST':
        try:
            # Detectar si es AJAX o POST normal
            data = json.loads(request.body) if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else request.POST
            altura = data.get('altura')
            peso = data.get('peso')
            fecha_nac = data.get('edad')  # Formato esperado YYYY-MM-DD
            objetivo = data.get('objetivo')

            # Validar campos obligatorios
            if not all([altura, peso, fecha_nac, objetivo]):
                msg = {'error': 'Todos los campos son obligatorios.'}
                return JsonResponse(msg, status=400) if request.headers.get('X-Requested-With') else redirect('userd')

            # Validar numéricos
            try:
                altura = float(altura)
                peso = float(peso)
                if altura <= 0 or peso <= 0:
                    msg = {'error': 'Altura y peso deben ser mayores a 0.'}
                    return JsonResponse(msg, status=400) if request.headers.get('X-Requested-With') else redirect('userd')
            except ValueError:
                msg = {'error': 'Altura y peso deben ser números válidos.'}
                return JsonResponse(msg, status=400) if request.headers.get('X-Requested-With') else redirect('userd')

            # Validar fecha
            try:
                fecha_nac_date = datetime.strptime(fecha_nac, '%Y-%m-%d').date()
            except ValueError:
                msg = {'error': 'Fecha de nacimiento inválida. Formato YYYY-MM-DD.'}
                return JsonResponse(msg, status=400) if request.headers.get('X-Requested-With') else redirect('userd')

            # Calcular edad en años
            hoy = date.today()
            edad_anios = hoy.year - fecha_nac_date.year - (
                (hoy.month, hoy.day) < (fecha_nac_date.month, fecha_nac_date.day)
            )
            if edad_anios < 0 or edad_anios > 150:
                msg = {'error': 'Edad fuera de rango.'}
                return JsonResponse(msg, status=400) if request.headers.get('X-Requested-With') else redirect('userd')

            # Validar objetivo
            valid_objetivos = [c[0] for c in DatosUsuario._meta.get_field('objetivo').choices]
            if objetivo not in valid_objetivos:
                msg = {'error': 'Objetivo inválido.'}
                return JsonResponse(msg, status=400) if request.headers.get('X-Requested-With') else redirect('userd')

            # Guardar historial si cambió peso o altura
            if datos_usuario.peso and datos_usuario.altura:
                if datos_usuario.peso != peso or datos_usuario.altura != altura:
                    HistorialPersonalUsuario.objects.create(
                        usuario=usuario,
                        peso_anterior=datos_usuario.peso or 0,
                        altura_anterior=datos_usuario.altura or 0
                    )

            # Actualizar datos
            datos_usuario.altura = altura
            datos_usuario.peso = peso
            datos_usuario.edad = fecha_nac_date
            datos_usuario.objetivo = objetivo
            datos_usuario.fecha_modificacion = timezone.now()
            datos_usuario.save()

            # Calcular IMC
            imc = None
            if datos_usuario.altura and datos_usuario.peso:
                try:
                    imc = round(float(datos_usuario.peso) / ((float(datos_usuario.altura) / 100) ** 2), 2)
                except Exception:
                    imc = None

            # Respuesta AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'imc': imc,
                    'edad_anios': edad_anios,
                    'altura': datos_usuario.altura,
                    'peso': datos_usuario.peso,
                    'objetivo': datos_usuario.objetivo,
                    'datos_usuario': {
                        'altura': datos_usuario.altura,
                        'peso': datos_usuario.peso,
                        'edad': edad_anios,
                        'objetivo': datos_usuario.objetivo
                    }
                })

            messages.success(request, 'Datos actualizados correctamente.')
            return redirect('userd')

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': str(e)}, status=500)
            messages.error(request, f'Error al actualizar: {str(e)}')
            return redirect('userd')

    # Calcular IMC inicial
    imc = round(datos_usuario.peso / ((datos_usuario.altura / 100) ** 2), 2) if datos_usuario.altura and datos_usuario.peso else None

    # Calcular edad para mostrar
    edad_anios = None
    if datos_usuario.edad:
        hoy = date.today()
        edad_anios = hoy.year - datos_usuario.edad.year - (
            (hoy.month, hoy.day) < (datos_usuario.edad.month, datos_usuario.edad.day)
        )

    return render(request, 'user.html', {
        'usuario': usuario,
        'datos_usuario': datos_usuario,
        'imc': imc,
        'edad_anios': edad_anios
    })



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