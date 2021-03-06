# Generated by Django 2.1.7 on 2019-02-19 03:28

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0032_auto_20190219_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(upload_to='photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='negocio',
            name='pet_aceitos',
            field=models.CharField(choices=[('dog', 'Cachorro'), ('cat', 'Gato'), ('bird', 'Pássaros'), ('fish', 'Peixes'), ('rep', 'Reptéis'), ('horse', 'Cavalos'), ('rat', 'Roedores')], default='dog', max_length=2),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='pet',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('dog', 'Cachorro'), ('cat', 'Gato'), ('bird', 'Pássaros'), ('fish', 'Peixes'), ('rep', 'Reptéis'), ('horse', 'Cavalos'), ('rat', 'Roedores')], max_length=30, verbose_name='Selecione seus pets'),
        ),
    ]
