# Generated by Django 3.0.4 on 2020-12-11 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ControlEscolar', '0002_auto_20201211_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adeudo',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='cantidad',
            field=models.IntegerField(default=None),
        ),
    ]