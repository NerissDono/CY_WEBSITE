# Generated by Django 5.1.7 on 2025-03-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_author_category_remove_article_contenu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(upload_to='data/covers/', verbose_name='Image de couverture'),
        ),
    ]
