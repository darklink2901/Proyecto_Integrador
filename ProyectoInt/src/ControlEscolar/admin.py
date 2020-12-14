from django.contrib import admin
from .models import Alumno,Laboratorio,Material,Adeudo
# Register your models here.
admin.site.register(Alumno)
admin.site.register(Laboratorio)
admin.site.register(Material)
admin.site.register(Adeudo)
