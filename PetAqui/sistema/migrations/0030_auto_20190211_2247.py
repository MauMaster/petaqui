# Generated by Django 2.1.5 on 2019-02-12 00:47

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0029_auto_20190211_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='negocio',
            name='pet_aceitos',
            field=models.CharField(choices=[('dog', 'Cachorro'), ('Cat', 'Gato'), ('bird', 'Pássaros'), ('fish', 'Peixes'), ('rep', 'Reptéis'), ('horse', 'Cavalos'), ('rat', 'Roedores')], default='dog', max_length=2),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='pet',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('dog', 'Cachorro'), ('Cat', 'Gato'), ('bird', 'Pássaros'), ('fish', 'Peixes'), ('rep', 'Reptéis'), ('horse', 'Cavalos'), ('rat', 'Roedores')], max_length=30, verbose_name='Selecione seus pets'),
        ),
    ]
