# Generated by Django 2.1.7 on 2019-05-16 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0052_auto_20190512_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='empresa',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='nota',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
    ]