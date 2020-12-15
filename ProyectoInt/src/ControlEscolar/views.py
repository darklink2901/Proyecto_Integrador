from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Adeudo,Material,Alumno,Laboratorio
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .utils import render_to_pdf
# Create your views here.

def inicio(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username = request.session["usr"] )
        departamento = usuario.perfil.departamento
        laboratorio = Laboratorio.objects.get(nombre = departamento)
        adeudosTotales = Adeudo.objects.filter(area = laboratorio).filter(cargo = True).count()
        materialDisponible = Material.objects.filter(area = laboratorio).count()
        contexto = {
            'departamento': departamento,
            'usuario': usuario,
            'adeudosTotales': adeudosTotales,
            'materialDisponible':materialDisponible
        }
        return render(request, "ControlEscolar/index.html",contexto)
    return redirect('login')

def generarPrestamo(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username = request.session["usr"] )
        departamento = usuario.perfil.departamento
        laboratorio = Laboratorio.objects.get(nombre = departamento)
        adeudosTotales = Adeudo.objects.filter(area = laboratorio).count()
        materialDisponible = Material.objects.filter(area = laboratorio).count
        materiales = Material.objects.filter(area = laboratorio)
        contexto = {
            'departamento': departamento,
            'usuario': usuario,
            'adeudosTotales': adeudosTotales,
            'materialDisponible':materialDisponible,
            'materiales':materiales
        }
        if request.POST.get('num') and request.POST.get('mat') and request.POST.get('can'):
            valor = int(request.POST.get('can'))
            post = Adeudo()
            alum = request.POST.get('num')
            alumno = Alumno.objects.get(numeroControl = alum) #Cambiar a .get si comienza a fallar
            if not alumno: #Eliminiar condicion si empieza a fallar
                messages.success(request, '¡¡Numero de control incorrecto!!')
                return redirect('generarPrestamo')
            mat = request.POST.get('mat')
            material = Material.objects.get(idMaterial = mat) #material especifico
            if material.cantidad >= valor:
                post.numeroControl = alumno
                post.material = material
                post.area = laboratorio
                post.cantidad = request.POST.get('can')
                post.historial = request.POST.get('can')
                post.cargo = True
                post.save()
                material.cantidad = material.cantidad - valor
                material.save()
                messages.success(request, '¡¡Prestamo realizado!!')
                return redirect('generarPrestamo')
            else:
                messages.warning(request, '¡¡No queda material suficiente para el prestamo (Material disponible: '+str(material.cantidad)+')!!')
                return redirect('generarPrestamo')
        if request.method == 'POST':
            messages.warning(request, '¡¡Por favor verifique todos los campos!!')
        return render(request, "ControlEscolar/generarPrestamo.html",contexto)
    return redirect('login')

def agregarMaterial(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username = request.session["usr"] )
        departamento = usuario.perfil.departamento
        laboratorio = Laboratorio.objects.get(nombre = departamento)
        adeudosTotales = Adeudo.objects.filter(area = laboratorio).count()
        materialDisponible = Material.objects.filter(area = laboratorio).count
        materiales = Material.objects.filter(area = laboratorio)
        contexto = {
            'departamento': departamento,
            'usuario': usuario,
            'adeudosTotales': adeudosTotales,
            'materialDisponible':materialDisponible,
            'materiales':materiales
        }
        if request.POST.get('nom') and request.POST.get('pre') and request.POST.get('can'):
            post = Material()
            post.nombre = request.POST.get('nom')
            post.area = laboratorio
            post.precio = request.POST.get('pre')
            post.cantidad = request.POST.get('can')
            post.save()
            messages.success(request, '¡¡Se añadió el material!!')
            return redirect('agregarMaterial')
        if request.method == 'POST':
            messages.warning(request, '¡¡Por favor verifique todos los campos!!')
        return render(request, "ControlEscolar/agregarMaterial.html",contexto)
    return redirect('login')

def materialDisponible(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username = request.session["usr"] )
        departamento = usuario.perfil.departamento
        laboratorio = Laboratorio.objects.get(nombre = departamento)
        adeudosTotales = Adeudo.objects.filter(area = laboratorio).count()
        materialDisponible = Material.objects.filter(area = laboratorio).count
        materiales = Material.objects.filter(area = laboratorio)
        contexto = {
            'departamento': departamento,
            'usuario': usuario,
            'adeudosTotales': adeudosTotales,
            'materialDisponible':materialDisponible,
            'materiales':materiales
        }
        return render(request, "ControlEscolar/materialDisponible.html",contexto)
    return redirect('login')

def recibirMaterial(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username = request.session["usr"] )
        departamento = usuario.perfil.departamento
        laboratorio = Laboratorio.objects.get(nombre = departamento)
        adeudosTotales = Adeudo.objects.filter(area = laboratorio).count()
        materialDisponible = Material.objects.filter(area = laboratorio).count
        materiales = Material.objects.filter(area = laboratorio)
        contexto = {
            'departamento': departamento,
            'usuario': usuario,
            'adeudosTotales': adeudosTotales,
            'materialDisponible':materialDisponible,
            'materiales':materiales
        }
        if request.POST.get('num') and request.POST.get('mat') and request.POST.get('can') and request.POST.get('numAd'):
            ad = request.POST.get('numAd')
            adeudo = Adeudo.objects.get(idAdeudo = ad)
            materialEsp = Material.objects.get(idMaterial = request.POST.get('mat'))
            valor = int(request.POST.get('can'))
            if adeudo.cantidad == valor:
                adeudo.cargo = False
                adeudo.cantidad = 0
                materialEsp.cantidad = materialEsp.cantidad + valor
                adeudo.save()
                materialEsp.save()
                messages.success(request, '¡¡Se elimino este adeudo!!')
                return redirect('recibirMaterial')
            if valor < adeudo.cantidad:
                adeudo.cantidad = adeudo.cantidad - valor
                materialEsp.cantidad = materialEsp.cantidad + valor
                adeudo.save()
                materialEsp.save()
                messages.warning(request, '¡¡El alumno aún debe: !!' + adeudo.material.nombre + '('+str(adeudo.cantidad)+')')
                return redirect('recibirMaterial')
            materialEsp.cantidad = materialEsp.cantidad + valor
            materialEsp.save()
            messages.success(request, '¡¡Se devolvió el material!!')
            return redirect('recibirMaterial')
        if request.method == 'POST':
            messages.warning(request, '¡¡Por favor verifique todos los campos!!')
        return render(request, "ControlEscolar/recibirMaterial.html",contexto)
    return redirect('login')

def todosPrestamos(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username = request.session["usr"] )
        departamento = usuario.perfil.departamento
        laboratorio = Laboratorio.objects.get(nombre = departamento)
        adeudosTotales = Adeudo.objects.filter(area = laboratorio).count()
        adeudos = Adeudo.objects.filter(area = laboratorio ).filter(cargo = True)
        materialDisponible = Material.objects.filter(area = laboratorio).count
        materiales = Material.objects.filter(area = laboratorio)
        queryset = request.GET.get("bus")
        if queryset:
            adeudos =Adeudo.objects.filter(
             Q(idAdeudo__icontains = queryset)|
             Q(numeroControl__numeroControl__icontains = queryset)
            ).filter(area = laboratorio).filter(cargo = True).distinct()
            contexto = {
                'departamento': departamento,
                'usuario': usuario,
                'adeudos': adeudos,
            }
            return render(request, "ControlEscolar/todosPrestamos.html",contexto)
        contexto = {
            'departamento': departamento,
            'usuario': usuario,
            'adeudosTotales': adeudosTotales,
            'materialDisponible':materialDisponible,
            'materiales':materiales,
            'adeudos':adeudos
        }
        return render(request, "ControlEscolar/todosPrestamos.html",contexto)
    return redirect('login')

def financieros(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username = request.session["usr"] )
        adeudos = Adeudo.objects.filter(cargo = True)
        departamento = usuario.perfil.departamento
        laboratorio = Laboratorio.objects.get(nombre = departamento)
        queryset = request.GET.get("bus")
        if queryset:
            adeudos =Adeudo.objects.filter(
             Q(idAdeudo__icontains = queryset)|
             Q(numeroControl__numeroControl__icontains = queryset)
            ).filter(cargo = True).distinct()
            contexto = {
                'departamento': departamento,
                'usuario': usuario,
                'adeudos': adeudos,
            }
            return render(request, "ControlEscolar/alumnosAdeudos.html",contexto)
        contexto = {
        'usuario': usuario,
        'adeudos':adeudos,
        'laboratorio': laboratorio,
        'departamento': departamento
        }
    return render(request, "ControlEscolar/alumnosAdeudos.html",contexto)

def liberar_alumno(request,num):
    alum = Alumno.objects.get(numeroControl = num)
    pdf = render_to_pdf('ControlEscolar/lista2.html', {'alum':alum})
    return HttpResponse(pdf, content_type='application/pdf')

def ficha_pago(request,id):
    adeudos = Adeudo.objects.get(idAdeudo = id)
    num = adeudos.numeroControl.numeroControl
    alum = Alumno.objects.get(numeroControl = num)
    costo = adeudos.material.precio * adeudos.cantidad
    contexto = {
        'alum': alum,
        'adeudos': adeudos,
        'costo':costo
    }
    pdf = render_to_pdf('ControlEscolar/lista.html', contexto)
    return HttpResponse(pdf, content_type='application/pdf')

def liberacion(request):
    if request.user.is_authenticated:
        adeudos = Adeudo.objects.filter(cargo = False)
        contexto = {
            'adeudos': adeudos
        }
    return render(request, "ControlEscolar/liberarAlumnos.html",contexto)
