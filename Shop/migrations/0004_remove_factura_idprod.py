# Generated by Django 4.0.6 on 2022-07-11 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0003_alter_factura_idusuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='idProd',
        ),
    ]
