# Generated by Django 2.1.7 on 2019-06-20 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0064_auto_20190620_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='negocio',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
