"""ProyectoInt URL Configuration

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
from django.urls import path
from InicioSesion.views import login,logout,registro
from ControlEscolar.views import inicio,generarPrestamo,agregarMaterial,materialDisponible,todosPrestamos,recibirMaterial,financieros,ficha_pago,liberar_alumno,liberacion
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/',inicio, name='inicio'),
    path('login/',login, name='login'),
    path('logout/',logout, name='logout'),
    path('registro/',registro, name='registro'),
    path('generarPrestamo/',generarPrestamo, name='generarPrestamo'),
    path('agregarMaterial/',agregarMaterial, name='agregarMaterial'),
    path('materialDisponible/',materialDisponible, name='materialDisponible'),
    path('recibirMaterial/',recibirMaterial, name='recibirMaterial'),
    path('todosPrestamos/',todosPrestamos, name='todosPrestamos'),
    path('financieros/',financieros, name='financieros'),
    path('ficha_pago/<int:id>',ficha_pago, name='ficha_pago'),
    path('liberacion/',liberacion, name='liberacion'),
    path('liberar_alumno/<int:num>',liberar_alumno, name='liberar_alumno'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
