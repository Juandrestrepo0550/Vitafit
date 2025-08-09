from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.utils import timezone
from datetime import date
from .models import Usuarios, DatosUsuario

@receiver(user_signed_up)
def crear_usuario_personalizado(sender, request, user, **kwargs):
    """
    Se ejecuta cuando un usuario se registra por Google o email.
    Crea un registro en la tabla 'usuarios' y en 'datos_usuario'.
    """
    if not Usuarios.objects.filter(correo=user.email).exists():
        nombre = user.first_name or 'Nombre'
        apellido = user.last_name or 'Apellido'
        correo = user.email

        # Crear usuario en tabla 'usuarios'
        nuevo_usuario = Usuarios.objects.create(
            nombres=nombre,
            apellidos=apellido,
            correo=correo,
            Edad=date(2000, 1, 1),  # Fecha de nacimiento por defecto
            contrasena=user.password,
            rol='user',
            estado='activo',
            fecha_registro=timezone.now(),
            fecha_modificacion=timezone.now()
        )

        # Crear registro en 'datos_usuario'
        DatosUsuario.objects.create(
            id_usuario=nuevo_usuario,
            edad=date(2000, 1, 1),  # fecha de nacimiento por defecto
            peso=0.0,
            altura=0.0,
            objetivo='maintenance'
        )
