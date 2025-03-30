from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_add_xp_level_to_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='xp_level',
            field=models.CharField(
                max_length=15,
                choices=[
                    ('simple', 'Simple'),
                    ('intermediate', 'Intermédiaire'),  # Nouveau niveau ajouté
                    ('complex', 'Complexe'),
                    ('admin', 'Admin'),
                ],
                default='simple',
                verbose_name="Niveau d'XP"
            ),
        ),
    ]
