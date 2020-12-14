from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

class FormLogin(forms.Form):
    usuario=forms.CharField(max_length=70)
    password=forms.CharField(widget = forms.PasswordInput, max_length=70)

class CustomUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']
