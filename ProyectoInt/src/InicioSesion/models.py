from django.db import models
from django.contrib.auth.models import AbstractUser #Importar modelo de login
from django.contrib.auth.models import User
# Create your models here.

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,primary_key = True)
    imagen = models.ImageField('Imagen de perfil', upload_to = 'perfil/', height_field = None, width_field = None, max_length = 200)
    departamento = models.CharField('Departamento asignado', max_length = 100)

    def __str__(self):
        return str(self.usuario)
