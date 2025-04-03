from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_xp_points'),  # Reference the latest migration
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_count',
            field=models.IntegerField(default=0, help_text="Nombre de connexions de l'utilisateur."),
        ),
    ]
