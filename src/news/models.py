from django.db import models

class Article():
    name= models.CharField(max_length=30, verbose_name= "nom")
    contenu=models.CharField(max_length= 4000, verbose_name="contenu")
    cover=models.ImageField(verbose_name="Image de couverture")

    class Meta():
        verbose_name="Article"
        verbose_name_plural="Articles"

