# Generated by Django 2.1.7 on 2019-03-09 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0047_auto_20190309_2331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gallery',
            old_name='usuario',
            new_name='usuario_id',
        ),
    ]
