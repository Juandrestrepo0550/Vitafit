from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta base
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),

    path('register/', views.register, name='register'),
    path('inicio_sesion/',views.inicio_sesion, name='inicio_sesion'),
    #path('adminpage/', views.adminpage, name='adminpage'), #9784e266c2f4109c726a77594b6737b054cab221
    path('logout/', views.cerrar_sesion, name='logout'),


    # path('login/', views.register, name='register'),

    path('adminpage/', views.adminpage, name='adminpage'),


]