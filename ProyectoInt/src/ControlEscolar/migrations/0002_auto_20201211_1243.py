# Generated by Django 3.0.4 on 2020-12-11 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ControlEscolar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='cantidad',
            field=models.IntegerField(default=True),
        ),
    ]
