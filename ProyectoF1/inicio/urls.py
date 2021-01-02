"""ProyectoF1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login),
    path('login/', views.login, name="login"),
    path('transferencia/', views.transferencia),
    path('solicitudprestamo/', views.prestamo, name="solicitarprestamo"),
    path('estadodecuenta/', views.estadoDeCeunta),
    path('infousr/', views.infoUsr, name="infousr"),
    path('logout/', views.logout, name="logout"),
    path('tarjeta/', views.tarjeta, name="tarjeta"),
    path('infoempresa/', views.infoEmpresa, name="infoempresa"),
    path('registroplanilla/', views.registroPlanilla, name="registroplanilla"),
    path('addempleadoplanilla/', views.addEmpleadoPlanilla, name="addempleadoplanilla"),
    path('cargarcsv/', views.CargarCSV, name="cargarcsv"),
    path('cargarcsv2/', views.cargarCSV2, name="seleccionarplanilla"),
]
