from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.utils import timezone
from .models import Usuarios


@receiver(user_signed_up)
def crear_usuario_personalizado(sender, request, user, **kwargs):
    print("✅ Señal recibida para:", user.email)  # Esto debe aparecer en la consola

    # resto del código...

@receiver(user_signed_up)
def crear_usuario_personalizado(sender, request, user, **kwargs):
    if not Usuarios.objects.filter(correo=user.email).exists():
        nombre = user.first_name or 'Nombre'
        apellido = user.last_name or 'Apellido'
        correo = user.email
        nickname = user.username

        nuevo_usuario = Usuarios(
            nombres=nombre,
            apellidos=apellido,
            correo=correo,
            nickname=nickname,
            Edad='2000-01-01',  # Fecha fija opcional
            peso=0.0,
            altura=0.0,
            contrasena=user.password,
            rol='user',
            estado='activo',
            fecha_registro=timezone.now(),
            fecha_modificacion=timezone.now()
        )
        nuevo_usuario.save()
