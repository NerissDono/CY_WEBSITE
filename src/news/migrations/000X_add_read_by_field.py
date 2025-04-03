from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('news', '000X_update_article_cover'),  # Replace with the latest migration
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='read_by',
            field=models.ManyToManyField(
                related_name='read_articles',
                to='user.User',
                blank=True,
                verbose_name="Utilisateurs ayant lu l'article"
            ),
        ),
    ]
