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
    nickname = models.CharField(max_length=20)  # Faltaba
    Edad = models.IntegerField()                   # Faltaba
    peso = models.DecimalField(max_digits=5, decimal_places=2)   # Faltaba
    altura = models.DecimalField(max_digits=5, decimal_places=2) # Faltaba
    objetivo = models.CharField(
        max_length=20,
        choices=[
            ('weight_loss', 'Pérdida de peso'),
            ('muscle_gain', 'Ganancia muscular'),
            ('endurance', 'Resistencia'),
            ('maintenance', 'Mantenimiento'),
        ],
        default='maintenance'
    )
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
    recuperarcontraseña = models.CharField(max_length=128, blank=True, null=True)
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