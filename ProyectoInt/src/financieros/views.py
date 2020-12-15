from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from ControlEscolar.models import Adeudo,Material,Alumno,Laboratorio
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def financieros(request):
    if request.user.is_authenticated:
        # usuario = User.objects.get(username = request.session["usr"] )
        # departamento = usuario.perfil.departamento
        # laboratorio = Laboratorio.objects.get(nombre = departamento)
        # adeudosTotales = Adeudo.objects.filter(area = laboratorio).filter(cargo = True).count()
        # materialDisponible = Material.objects.filter(area = laboratorio).count()
        # contexto = {
        #     'departamento': departamento,
        #     'usuario': usuario,
        #     'adeudosTotales': adeudosTotales,
        #     'materialDisponible':materialDisponible
        # }
        return render(request, "financieros/index.html")
    return redirect('login')
