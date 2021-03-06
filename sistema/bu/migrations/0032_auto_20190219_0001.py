# Generated by Django 2.1.7 on 2019-02-19 00:01

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0031_auto_20190212_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='negocio',
            name='pet_aceitos',
            field=models.CharField(choices=[('dog', 'Cachorro'), ('https://www.petz.com.br/blog/wp-content/uploads/2017/07/gato02.jpg', 'cat'), ('bird', 'Pássaros'), ('fish', 'Peixes'), ('rep', 'Reptéis'), ('horse', 'Cavalos'), ('rat', 'Roedores')], default='dog', max_length=2),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='pet',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('dog', 'Cachorro'), ('https://www.petz.com.br/blog/wp-content/uploads/2017/07/gato02.jpg', 'cat'), ('bird', 'Pássaros'), ('fish', 'Peixes'), ('rep', 'Reptéis'), ('horse', 'Cavalos'), ('rat', 'Roedores')], max_length=100, verbose_name='Selecione seus pets'),
        ),
    ]
