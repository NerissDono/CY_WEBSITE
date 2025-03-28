from django.db import models

class ObjConnecte(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom')
    type = models.ForeignKey('Type', on_delete=models.DO_NOTHING, verbose_name='Type')
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(upload_to='data/objConnecte_images/', default='data/objConnecte_images/default.jpg', verbose_name='Image')
    date = models.DateTimeField(auto_now_add=True)
    state=models.BooleanField(default=False, verbose_name='Etat')
    #user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, verbose_name='Utilisateur')
    connected=models.BooleanField(default=False, verbose_name='Connecté')
    ip=models.GenericIPAddressField(verbose_name='Adresse IP', default='127.0.0.1')  # Correction
    #port=models.IntegerField(verbose_name='Port')
    longitude=models.FloatField(verbose_name='Longitude', default=0.0)  # Correction
    latitude=models.FloatField(verbose_name='Latitude', default=0.0)  # Correction

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Objet connecté'
        verbose_name_plural = 'Objets connectés'

class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'