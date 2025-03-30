from objConnecte.models import Type, ObjConnecte
from django.utils import timezone
import random

# Creation des types d'objets connectes
types_data = [
    {
        'name': 'Feux tricolores',
        'description': 'Feux de signalisation pour reguler le trafic routier',
    },
    {
        'name': 'Lampadaires',
        'description': 'Eclairage public intelligent avec variation d\'intensite',
    },
    {
        'name': 'Trottinettes electriques',
        'description': 'Trottinettes en libre-service localisables via GPS',
    },
    {
        'name': 'Capteurs de pollution',
        'description': 'Mesure de la qualite de l\'air et des particules fines',
    },
]

# Supprimer tous les objets connectés
print("Suppression des objets connectés...")
count, details = ObjConnecte.objects.all().delete()
print(f"Supprimé {count} objets avec succès.")

# Creer ou mettre a jour les types
for type_data in types_data:
    Type.objects.update_or_create(
        name=type_data['name'],
        defaults={'description': type_data['description']}
    )
    print(f"Type cree: {type_data['name']}")

# Recuperer les types crees
feu_type = Type.objects.get(name='Feux tricolores')
lampadaire_type = Type.objects.get(name='Lampadaires')
trottinette_type = Type.objects.get(name='Trottinettes electriques')
capteur_type = Type.objects.get(name='Capteurs de pollution')

# Creer des objets connectes - Feux tricolores
feux_data = [
    {
        'name': 'Feu Place de la Mairie',
        'type': feu_type,
        'description': 'Feu tricolore principal regulant le carrefour devant la mairie',
        'image': 'data/objConnecte_images/default.jpg',
        'state': True,
        'connected': True,
        'ip': '192.168.1.10',
        'longitude': 2.2098,
        'latitude': 48.8969,
    },
    {
        'name': 'Feu Avenue de la Republique',
        'type': feu_type,
        'description': 'Feu tricolore situe au croisement de l\'avenue principale',
        'image': 'data/objConnecte_images/default.jpg',
        'state': True,
        'connected': True,
        'ip': '192.168.1.11',
        'longitude': 2.2065,
        'latitude': 48.8985,
    },
]

# Creer des objets connectes - Lampadaires
lampadaires_data = [
    {
        'name': 'Lampadaire Parc Central',
        'type': lampadaire_type,
        'description': 'Lampadaire intelligent a LED avec capteur de presence',
        'image': 'data/objConnecte_images/default.jpg',
        'state': False,
        'connected': True,
        'ip': '192.168.2.10',
        'longitude': 2.2150,
        'latitude': 48.8950,
    },
    {
        'name': 'Lampadaire Rue des Ecoles',
        'type': lampadaire_type,
        'description': 'Lampadaire solaire avec stockage d\'energie integre',
        'image': 'data/objConnecte_images/default.jpg',
        'state': True,
        'connected': True,
        'ip': '192.168.2.11',
        'longitude': 2.2175,
        'latitude': 48.8925,
    },
]

# Creer des objets connectes - Trottinettes
trottinettes_data = [
    {
        'name': 'Trottinette #T2022-01',
        'type': trottinette_type,
        'description': 'Trottinette electrique localisable en temps reel, autonomie 25km',
        'image': 'data/objConnecte_images/default.jpg',
        'state': True,
        'connected': False,
        'ip': '192.168.3.10',
        'longitude': 2.2156,
        'latitude': 48.8987,
    },
    {
        'name': 'Trottinette #T2022-05',
        'type': trottinette_type,
        'description': 'Trottinette electrique avec batterie amovible, autonomie 30km',
        'image': 'data/objConnecte_images/default.jpg',
        'state': False,
        'connected': True,
        'ip': '192.168.3.11',
        'longitude': 2.2198,
        'latitude': 48.8995,
    },
]

# Creer des objets connectes - Capteurs
capteurs_data = [
    {
        'name': 'Capteur Qualite Air Centre-ville',
        'type': capteur_type,
        'description': 'Mesure des particules fines PM2.5 et PM10, ainsi que le CO2',
        'image': 'data/objConnecte_images/default.jpg',
        'state': True,
        'connected': True,
        'ip': '192.168.4.10',
        'longitude': 2.2120,
        'latitude': 48.8960,
    },
    {
        'name': 'Capteur Pollution Sonore Gare',
        'type': capteur_type,
        'description': 'Mesure des niveaux sonores aux abords de la gare ferroviaire',
        'image': 'data/objConnecte_images/default.jpg',
        'state': True,
        'connected': True,
        'ip': '192.168.4.11',
        'longitude': 2.2080,
        'latitude': 48.8990,
    },
]

# Creer tous les objets connectes
all_objects_data = feux_data + lampadaires_data + trottinettes_data + capteurs_data

for obj_data in all_objects_data:
    # Verifier si l'objet existe deja
    obj, created = ObjConnecte.objects.get_or_create(
        name=obj_data['name'],
        defaults={
            'type': obj_data['type'],
            'description': obj_data['description'],
            'image': obj_data['image'],
            'state': obj_data['state'],
            'connected': obj_data['connected'],
            'ip': obj_data['ip'],
            'longitude': obj_data['longitude'],
            'latitude': obj_data['latitude'],
        }
    )
    if created:
        print(f"Objet cree: {obj.name}")
    else:
        print(f"Objet existant mis a jour: {obj.name}")

print("Importation terminee!")