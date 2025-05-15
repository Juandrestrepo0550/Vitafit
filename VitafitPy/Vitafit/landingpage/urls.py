from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta base
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('val_correo/', views.val_correo, name='val_correo'),
    path('inicio_sesion/',views.inicio_sesion, name='inicio_sesion'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('adminpage/', views.adminpage, name='adminpage'),
]