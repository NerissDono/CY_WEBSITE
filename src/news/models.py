from datetime import timezone
from django.db import models
from django.utils.html import mark_safe
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de l'auteur", unique=True)
    email = models.EmailField(verbose_name="Email de l'auteur")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    cover = models.ImageField(
        upload_to='article_covers/',
        blank=True,  # Allow blank values
        null=True,   # Allow null values
        help_text="Téléchargez une image de couverture pour l'article (optionnel)."
    )
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name="Catégorie")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Auteur")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    read_by = models.ManyToManyField(
        'user.User',
        related_name='read_articles',
        blank=True,
        verbose_name="Utilisateurs ayant lu l'article"
    )
    def image_preview(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url}" width="100" height="100" />')
        return "Pas d'image"
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name='comments', verbose_name="Article")
    name = models.CharField(max_length=100, verbose_name="Nom", blank=True)
    email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Contenu")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return f'Commentaire de {self.name} sur {self.article}'

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"