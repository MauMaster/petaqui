# Generated by Django 2.1.5 on 2019-01-08 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0011_usuario_pet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='foto',
        ),
    ]