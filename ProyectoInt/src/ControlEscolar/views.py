from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Adeudo,Material,Alumno,Laboratorio
from django.contrib import messages
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
        return render(request, "index.html",contexto)
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
        return render(request, "generarPrestamo.html",contexto)
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
        return render(request, "agregarMaterial.html",contexto)
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
        return render(request, "materialDisponible.html",contexto)
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
        return render(request, "recibirMaterial.html",contexto)
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
        contexto = {
            'departamento': departamento,
            'usuario': usuario,
            'adeudosTotales': adeudosTotales,
            'materialDisponible':materialDisponible,
            'materiales':materiales,
            'adeudos':adeudos
        }
        return render(request, "todosPrestamos.html",contexto)
    return redirect('login')
