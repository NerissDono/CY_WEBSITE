# Generated by Django 5.1.7 on 2025-03-23 12:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.CreateModel(
            name='ObjConnecte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.TextField(verbose_name='Description')),
                ('image', models.ImageField(default='data/objConnecte_images/default.jpg', upload_to='data/objConnecte_images/', verbose_name='Image')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='objConnecte.type', verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Objet connecté',
                'verbose_name_plural': 'Objets connectés',
            },
        ),
    ]
