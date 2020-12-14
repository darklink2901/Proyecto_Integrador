# Generated by Django 3.0.4 on 2020-12-11 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('numeroControl', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Numero de control')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('carrera', models.CharField(max_length=30, verbose_name='Carrera')),
                ('semestre', models.IntegerField(verbose_name='Semestre')),
            ],
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('codigoLaboratorio', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Codigo de Laboratorio')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de Laboratorio')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('idMaterial', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de material')),
                ('precio', models.FloatField(verbose_name='Precio')),
                ('cantidad', models.IntegerField(default=None)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlEscolar.Laboratorio')),
            ],
        ),
        migrations.CreateModel(
            name='Adeudo',
            fields=[
                ('idAdeudo', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=None)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlEscolar.Laboratorio', verbose_name='Area')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlEscolar.Material')),
                ('numeroControl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ControlEscolar.Alumno')),
            ],
        ),
    ]
