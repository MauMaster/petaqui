# Generated by Django 2.1.7 on 2019-04-28 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0045_auto_20190428_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='nome',
        ),
    ]