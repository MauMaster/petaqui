# Generated by Django 2.1.7 on 2019-04-10 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0010_auto_20190410_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='negocio',
            new_name='id_negocio',
        ),
    ]
