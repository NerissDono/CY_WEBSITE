# Generated by Django 5.1.7 on 2025-03-27 17:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objConnecte', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='objconnecte',
            name='connected',
            field=models.BooleanField(default=False, verbose_name='Connecté'),
        ),
        migrations.AddField(
            model_name='objconnecte',
            name='ip',
            field=models.GenericIPAddressField(default=django.utils.timezone.now, verbose_name='Adresse IP'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objconnecte',
            name='latitude',
            field=models.FloatField(default=django.utils.timezone.now, verbose_name='Latitude'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objconnecte',
            name='longitude',
            field=models.FloatField(default=django.utils.timezone.now, verbose_name='Longitude'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objconnecte',
            name='state',
            field=models.BooleanField(default=False, verbose_name='Etat'),
        ),
    ]
