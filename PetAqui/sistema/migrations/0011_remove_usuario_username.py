# Generated by Django 2.1.5 on 2019-01-28 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0010_usuario_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='username',
        ),
    ]
