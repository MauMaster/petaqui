# Generated by Django 2.1.7 on 2019-04-11 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sistema', '0026_auto_20190411_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='cnpj',
        ),
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(default=99, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
