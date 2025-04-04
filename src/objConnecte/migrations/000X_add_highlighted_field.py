from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
    ('objConnecte', '0004_type_icon'),  # Replace with the correct last migration name
    ]

    operations = [
        migrations.AddField(
            model_name='objconnecte',
            name='highlighted',
            field=models.BooleanField(default=False, verbose_name='Marqué'),
        ),
    ]
