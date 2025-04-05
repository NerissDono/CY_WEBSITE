import unicodedata
import random
from datetime import datetime, timedelta
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

    def generate_usage_data(self, start_date, end_date):
        """Génère des données d'utilisation simulées pour la période spécifiée"""
        data = []
        current_date = start_date
        while current_date <= end_date:
            # Simuler différents types de données selon le type d'objet
            type_nom = self.type.name.lower()
            
            if "lampadaire" in type_nom:
                # Simuler la consommation énergétique (en kWh)
                # Plus forte la nuit, plus faible le jour
                hour = current_date.hour
                if hour >= 20 or hour < 6:  # Nuit
                    usage = random.uniform(0.4, 0.6)  # kWh
                else:  # Jour
                    usage = random.uniform(0.0, 0.1)  # kWh
                data_type = "energy_consumption"
                
            elif "feu" in type_nom:
                # Simuler la consommation énergétique pour les feux tricolores
                usage = random.uniform(0.2, 0.3)  # kWh
                data_type = "energy_consumption"
                
            elif "capteur" in type_nom:
                if "pollution" in type_nom:
                    # Simuler les niveaux de pollution (AQI)
                    usage = random.uniform(30, 80)
                    data_type = "pollution_level"
                else:
                    # Autres capteurs - consommation de batterie
                    usage = random.uniform(0.05, 0.1)  # kWh
                    data_type = "battery_consumption"
                
            elif "trottinette" in type_nom:
                # Simuler le niveau de batterie (%)
                usage = random.uniform(30, 100)
                data_type = "battery_level"
                
            else:
                # Par défaut, consommation énergétique
                usage = random.uniform(0.1, 0.3)
                data_type = "energy_consumption"
            
            # Ajouter des variations hebdomadaires
            if current_date.weekday() >= 5:  # Weekend
                usage *= 0.8  # Moins d'utilisation le weekend
                
            # Ajouter une entrée à notre liste de données
            data.append({
                'date': current_date,
                'value': round(usage, 2),
                'type': data_type
            })
            
            # Passer à l'heure suivante
            current_date += timedelta(hours=1)
            
        return data

    def get_energy_consumption(self, period='day'):
        """
        Retourne la consommation énergétique totale pour la période spécifiée
        period: 'day', 'week', 'month'
        """
        today = datetime.now()
        
        if period == 'day':
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif period == 'week':
            start_date = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today
        elif period == 'month':
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = today
        else:
            raise ValueError("Période non valide. Utilisez 'day', 'week', ou 'month'")
        
        # Générer des données simulées
        usage_data = self.generate_usage_data(start_date, end_date)
        
        # Calculer la consommation totale (en considérant seulement la consommation énergétique)
        energy_data = [item for item in usage_data if item['type'] == 'energy_consumption']
        total_consumption = sum(item['value'] for item in energy_data)
        
        # Ajuster la consommation pour les feux tricolores
        if 'feu' in self.type.name.lower():
            if period == 'month':
                total_consumption = 143.7  # Fixer la consommation mensuelle à 143.7 kWh
            elif period == 'week':
                total_consumption = 143.7 / 4  # Consommation hebdomadaire approximative
            elif period == 'day':
                total_consumption = 143.7 / 30  # Consommation journalière approximative
        
        return {
            'total': round(total_consumption, 2),
            'unit': 'kWh',
            'period': period,
            'data': energy_data
        }

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


class UsageData(models.Model):
    """Modèle pour stocker les données d'utilisation des objets connectés"""
    obj_connecte = models.ForeignKey(ObjConnecte, on_delete=models.CASCADE, related_name='usage_data')
    timestamp = models.DateTimeField()
    data_type = models.CharField(max_length=50, choices=[
        ('energy_consumption', 'Consommation énergétique'),
        ('pollution_level', 'Niveau de pollution'),
        ('battery_level', 'Niveau de batterie'),
        ('battery_consumption', 'Consommation de batterie'),
        ('usage_count', 'Nombre d\'utilisations'),
        ('uptime', 'Temps de fonctionnement'),
    ])
    value = models.FloatField()
    unit = models.CharField(max_length=20, default='kWh')
    
    class Meta:
        verbose_name = "Donnée d'utilisation"
        verbose_name_plural = "Données d'utilisation"
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.obj_connecte.name} - {self.get_data_type_display()}: {self.value} {self.unit} ({self.timestamp})"
