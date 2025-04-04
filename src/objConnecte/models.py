import unicodedata
from datetime import datetime
from django.db import models


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
    highlighted = models.BooleanField(default=False, verbose_name="Marqué")

    def __str__(self):
        return self.name

    @property
    def statut_dynamique(self):
        heure = datetime.now().hour

        def normalize(txt):
            return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8').lower()

        type_nom = normalize(self.type.name)

        if not self.connected:
            return "En panne (technicien requis)" if self.attente_technicien else "Déconnecté"

        if not self.state:
            if type_nom == "lampadaires":
                return "Éteint (manuel)" if heure >= 20 or heure < 6 else "Éteint (jour)"
            elif type_nom == "feux tricolores":
                return "Désactivé"
            elif type_nom == "caméras":
                return "Hors service"
            elif type_nom == "capteurs de pollution":
                return "En veille"
            elif type_nom == "trottinettes electriques":
                return "Stationnée"
            else:
                return "Inactif"

        # Si l'objet est actif et connecté :
        if type_nom == "lampadaires":
            return "Allumé" if heure >= 20 or heure < 6 else "Éteint (jour)"

        elif type_nom == 'feux tricolores':
            total_cycle = 40
            total_seconds = datetime.now().timestamp()  # temps en secondes depuis 1970
            seconds = int(total_seconds) % total_cycle
            if seconds < 20:
                return "Vert"
            elif seconds < 25:
                return "Orange"
            else:
                return "Rouge"

        elif type_nom == "caméras":
            return "Fonctionnelle"

        elif type_nom == "capteurs de pollution":
            return "Mesure active"

        elif type_nom == "trottinettes electriques":
            return "En circulation"

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
