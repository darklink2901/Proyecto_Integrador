from django.shortcuts import render
from django.contrib.auth import login as do_login
from .forms import FormLogin,CustomUserForm
from django.shortcuts import render,redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib import messages
from .models import Perfil

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.POST.get('usr') and request.POST.get('pwd'):
        usuario = request.POST.get('usr')
        password = request.POST.get('pwd')
        user = authenticate(username=usuario, password=password)
        if user is not None:
            request.session['usr'] = user.username
                # request.session['dep'] = user.departamento
            do_login(request, user)
            return redirect('inicio')
        else:
            messages.warning(request, '¡¡Por favor verifique las credenciales!!')
    if request.method == 'POST':
        messages.warning(request, '¡¡Por favor complete los campos!!')
    return render(request, "login.html")

def logout(request):
    do_logout(request)
    return redirect('login')

def registro(request):
    form = CustomUserForm()
    post = Perfil()
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        post = Perfil(request.POST)
        if form.is_valid() and request.POST.get('dep') and request.POST.get('ima'):
            form.save()
            post.departamento = request.POST.get('dep')
            post.imagen = request.POST.get('ima')
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username = username, password = password)
            usarito = User.objects.get(username = user.username)
            post.usuario = usarito
            post.save()
            messages.success(request, '¡¡Usuario creado con exito!!')
            request.session['usr'] = user.username
            do_login(request,user)
            return redirect('inicio')

    return render(request, "registro.html", {'form': form})
