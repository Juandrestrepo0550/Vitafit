# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class Usuarios(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     nombres = models.CharField(max_length=128)
#     apellidos = models.CharField(max_length=128)
#     correo = models.CharField(max_length=200)
#     contrasena = models.CharField(max_length=128)
#     rol = models.CharField(max_length=13)
#     foto_perfil = models.CharField(max_length=255, blank=True, null=True)
#     fecha_registro = models.DateTimeField(blank=True, null=True)
#     fecha_modificacion = models.DateTimeField(blank=True, null=True)
#     recuperarcontrasena = models.CharField(max_length=128, blank=True, null=True)
#     token = models.CharField(max_length=128, blank=True, null=True)
#     token_expiracion = models.DateTimeField(blank=True, null=True)
#     estado = models.CharField(max_length=8)
    
#     class Meta:
#         managed = False
#         db_table = 'usuarios'


from django.db import models
from django.db.models import F, Count
from django.utils import timezone


class Usuarios(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=128)
    apellidos = models.CharField(max_length=128)
    correo = models.CharField(max_length=200)
    Edad = models.DateField(null=True, blank=True)                 # Faltaba
    contrasena = models.CharField(max_length=128)
    rol = models.CharField(
        max_length=13,
        choices=[
            ('admin', 'admin'),
            ('user', 'user'),
            ('trainer', 'trainer'),
            ('nutricionista', 'nutricionista'),
        ],
        default='user'
    )
    #foto_perfil = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    recuperarcontrasena = models.CharField(max_length=128, blank=True, null=True)
    token = models.CharField(max_length=128, blank=True, null=True)
    token_expiracion = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=8,
        choices=[
            ('activo', 'activo'),
            ('inactivo', 'inactivo'),
        ],
        default='activo'
    )

    class Meta:
        managed = True  # porque ya tienes la tabla creada en MySQL
        db_table = 'usuarios'
        
class HistorialPersonalUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    peso_anterior = models.DecimalField(max_digits=5, decimal_places=2)
    altura_anterior = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'historial_personal_usuario'
        
from datetime import date
from django.db import models

class DatosUsuario(models.Model):
    id = models.AutoField(primary_key=True) 
    # usaremos OneToOne para que cada usuario tenga a lo sumo 1 fila en datos_usuario:
    id_usuario = models.OneToOneField(
        'Usuarios',
        on_delete=models.CASCADE,
        db_column='usuario_id',
        related_name='datos'
    )
    # guardamos fecha de nacimiento como DATE en la columna 'edad' (coincide con tu SQL actual)
    edad = models.DateField(null=True, blank=True, default=date(2000,1,1))   # <-- aquí guardas 2006-07-16
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00)
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00)

    objetivo = models.CharField(
        max_length=20,
        choices=[
            ('weight_loss', 'Pérdida de peso'),
            ('muscle_gain', 'Ganancia muscular'),
            ('endurance', 'Resistencia'),
            ('maintenance', 'Mantenimiento'),
        ],
        null=True,
        blank=True,
        default='maintenance'
    )

    class Meta:
        db_table = 'datos_usuario'
        managed = True   # recomendado para usar migraciones; ver nota abajo

    def __str__(self):
        return f"DatosUsuario({self.id_usuario.nombres})"

    @property
    def edad_anios(self) -> int | None:
        """
        Devuelve la edad en años (entero), calculada a partir de self.edad (DATE).
        Retorna None si no hay fecha de nacimiento.
        """
        if not self.edad:
            return None
        today = date.today()
        years = today.year - self.edad.year - (
            (today.month, today.day) < (self.edad.month, self.edad.day)
        )
        return years        


class Ejercicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    aporte_muscular = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Rutina(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    ejercicios = models.ManyToManyField(
        Ejercicio,
        through='RutinaEjercicio',
        related_name='rutinas',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    @property
    def cantidad_ejercicios(self):
        return self.rutinaejercicio_set.count()

class RutinaEjercicio(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    cantidad_ejercicios = models.PositiveSmallIntegerField(default=1)  # si es repeticiones o similar
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']
        unique_together = ('rutina', 'ejercicio')

    def __str__(self):
        return f"{self.rutina.nombre} - {self.ejercicio.nombre} (x{self.cantidad_ejercicios})"