# Generated by Django 2.1.7 on 2019-04-07 18:20

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0005_auto_20190407_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='galerry_usuario',
            field=stdimage.models.StdImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
