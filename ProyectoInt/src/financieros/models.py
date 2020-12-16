from django.db import models

# Create your models here.
class Alumno(models.Model):
    numeroControl = models.CharField(primary_key = True, max_length=20, verbose_name="Numero de control")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellidos = models.CharField(max_length=50, verbose_name="Apellidos")
    carrera = models.CharField(max_length=30, verbose_name="Carrera")
    semestre=models.IntegerField(verbose_name="Semestre")

    def __str__(self):
        return str(self.numeroControl)

class Laboratorio(models.Model):
    codigoLaboratorio = models.CharField(primary_key = True, max_length=20, verbose_name="Codigo de Laboratorio")
    nombre = models.CharField( max_length=50, verbose_name="Nombre de Laboratorio")

    def __str__(self):
        return self.nombre
    # adeudos = falta relacion

class Material(models.Model):
    idMaterial = models.AutoField(primary_key = True, unique = True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre de material")
    area = models.ForeignKey(Laboratorio, on_delete = models.CASCADE)
    precio = models.FloatField(verbose_name="Precio")
    cantidad = models.IntegerField(default = None)

    def __str__(self):
        return self.nombre

class Adeudo(models.Model):
    idAdeudo = models.AutoField(primary_key = True, unique = True)
    numeroControl = models.ForeignKey(Alumno, on_delete = models.CASCADE)
    material = models.ForeignKey(Material, on_delete = models.CASCADE)
    area = models.ForeignKey(Laboratorio, on_delete = models.CASCADE, verbose_name="Area")
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    cargo = models.BooleanField(default = None, verbose_name="Debe")
    historial = models.IntegerField(default = None)

    def __str__(self):
        return "Adeudo numero: " + str(self.idAdeudo)
