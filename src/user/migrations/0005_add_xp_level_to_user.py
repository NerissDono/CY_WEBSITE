from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_options_alter_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='xp_level',
            field=models.CharField(
                max_length=10,
                choices=[('simple', 'Simple'), ('complex', 'Complexe'), ('admin', 'Admin')],
                default='simple',
                verbose_name="Niveau d'XP"
            ),
        ),
    ]
