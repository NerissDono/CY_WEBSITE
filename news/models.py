from datetime import timezone
from django.db import models

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
    cover = models.ImageField(upload_to='data/covers/', verbose_name="Image de couverture", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name="Catégorie")
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, verbose_name="Auteur")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")

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