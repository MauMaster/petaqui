# Generated by Django 2.1.7 on 2019-02-24 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0042_auto_20190224_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='about',
            field=models.CharField(max_length=1000, verbose_name='Sobre você'),
        ),
    ]
