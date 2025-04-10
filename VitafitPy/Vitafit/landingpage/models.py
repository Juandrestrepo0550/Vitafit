# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Usuarios(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=128)
    apellidos = models.CharField(max_length=128)
    correo = models.CharField(max_length=200)
    nickname = models.CharField(max_length=20)
    edad = models.DateField(db_column='Edad')  # Field name made lowercase.
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    contrasena = models.CharField(max_length=128)
    rol = models.CharField(max_length=13)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    recuperarcontrasena = models.CharField(max_length=128, blank=True, null=True)
    token = models.CharField(max_length=128, blank=True, null=True)
    token_expiracion = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'usuarios'
