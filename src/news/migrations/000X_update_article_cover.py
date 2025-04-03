from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_article_author'),  # Replace with the latest migration in the `news` app
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(
                upload_to='article_covers/',
                blank=True,
                null=True,
                help_text="Téléchargez une image de couverture pour l'article (optionnel)."
            ),
        ),
    ]
