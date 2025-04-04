from django.db import models
from datetime import datetime
import unicodedata


class ObjConnecte(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom')
    type = models.ForeignKey('Type', on_delete=models.DO_NOTHING, verbose_name='Type')
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(upload_to='data/objConnecte_images/', default='data/objConnecte_images/default.jpg', verbose_name='Image')
    date = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=False, verbose_name='État')
    connected = models.BooleanField(default=False, verbose_name='Connecté')
    attente_technicien = models.BooleanField(default=False, verbose_name='Attente d’un technicien')
    ip = models.GenericIPAddressField(verbose_name='Adresse IP', default='127.0.0.1')
    longitude = models.FloatField(verbose_name='Longitude', default=0.0)
    latitude = models.FloatField(verbose_name='Latitude', default=0.0)

    def __str__(self):
        return self.name

    @property
    def statut_dynamique(self):
        heure = datetime.now().hour

        # Supprimer les accents et mettre en minuscule
        def normalize(txt):
            return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8').lower()

        type_nom = normalize(self.type.name)

        if type_nom == 'lampadaires':
            if not self.connected:
                return "En panne (technicien requis)" if self.attente_technicien else "Déconnecté"
            elif heure >= 20 or heure < 6:
                return "Allumé" if self.state else "Éteint (manuel)"
            else:
                return "Éteint (jour)"

        elif type_nom == 'feux tricolores':
            total_cycle = 40
            seconds = datetime.now().second % total_cycle
            if seconds < 20:
                return "Vert"
            elif seconds < 25:
                return "Orange"
            else:
                return "Rouge"

        elif type_nom == 'cameras':
            if not self.connected:
                return "Hors service" if self.attente_technicien else "Déconnectée"
            return "Fonctionnelle"

        elif type_nom == 'capteurs de pollution':
            return "Mesure active" if self.connected else "Déconnecté"

        elif type_nom == 'trottinettes electriques':
            if not self.connected:
                return "Hors ligne"
            elif self.state:
                return "En circulation"
            else:
                return "Stationnée"

        return "Statut inconnu"

    class Meta:
        verbose_name = 'Objet connecté'
        verbose_name_plural = 'Objets connectés'


class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom')
    description = models.TextField(verbose_name='Description')
    icon = models.ImageField(upload_to='data/type_images/', default='data/type_images/default.jpg', verbose_name='Icône')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'
