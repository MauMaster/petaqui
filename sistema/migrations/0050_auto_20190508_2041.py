# Generated by Django 2.1.7 on 2019-05-08 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0049_auto_20190508_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='nota',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=255, null=True),
        ),
    ]
