from django.urls import path
from .views import chat_api
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta base
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('val_correo/', views.val_correo, name='val_correo'),
    path('inicio_sesion/',views.inicio_sesion, name='inicio_sesion'),
    path('logout/', views.cerrar_sesion, name='logout'),    #path('adminpage/', views.adminpage, name='adminpage'), #9784e266c2f4109c726a77594b6737b054cab221
    #path('logout/', views.cerrar_sesion, name='logout'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('rutines/', views.rutines, name='rutines'),
    path('recomendaciones/', views.recomendaciones_vi, name='recomendaciones'),
    path('api/chat/', views.chat_api, name="chat_api"),
    path('userd/', views.userd, name='userd' )
    
]