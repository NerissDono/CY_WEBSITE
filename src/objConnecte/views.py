from django.shortcuts import render
from django.db.models import Q
from .models import ObjConnecte, Type
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Type

def index(request):
    # Statistiques pour la page d'accueil
    total_objects = ObjConnecte.objects.count()
    connected_objects = ObjConnecte.objects.filter(connected=True).count()
    active_objects = ObjConnecte.objects.filter(state=True).count()
    types_count = Type.objects.count()
    types = Type.objects.all()

    context = {
        'total_objects': total_objects,
        'connected_objects': connected_objects,
        'active_objects': active_objects,
        'types_count': types_count,
        'types': types,
    }
    return render(request, 'objConnecte/index.html', context)

def objets(request):
    # Récupération des paramètres de filtrage
    search_query = request.GET.get('search', '')
    type_id = request.GET.get('type', '')
    status = request.GET.get('status', '')
    
    # Récupération de tous les objets
    objets = ObjConnecte.objects.all()
    
    # Filtrage par recherche
    if search_query:
        objets = objets.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(type__name__icontains=search_query)
        )
    
    # Filtrage par type
    if type_id:
        objets = objets.filter(type_id=type_id)
    
    # Filtrage par statut
    if status:
        if status == 'connected':
            objets = objets.filter(connected=True)
        elif status == 'disconnected':
            objets = objets.filter(connected=False)
        elif status == 'active':
            objets = objets.filter(state=True)
        elif status == 'inactive':
            objets = objets.filter(state=False)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(objets, 9)  # 9 objets par page
    
    try:
        objets = paginator.page(page)
    except PageNotAnInteger:
        objets = paginator.page(1)
    except EmptyPage:
        objets = paginator.page(paginator.num_pages)
    
    # Récupérer tous les types pour le filtre
    types = Type.objects.all()
    
    context = {
        'objets': objets,
        'types': types,
        'search_query': search_query,
        'type_id': type_id,
        'status': status,
    }
    
    return render(request, 'objConnecte/objets.html', context)

def objet(request, id):
    objet = ObjConnecte.objects.get(id=id)
    return render(request, 'objConnecte/objet.html', {'objet': objet})

@login_required
@require_POST
def toggle_state(request, id):
    """Change l'état (actif/inactif) d'un objet connecté"""
    try:
        obj = ObjConnecte.objects.get(id=id)
        # Vérification des permissions
        if request.user.xp_level not in ['intermediate', 'complex', 'admin']:
            return JsonResponse({'success': False, 'message': 'Permissions insuffisantes'}, status=403)
        
        # Changement d'état
        obj.state = not obj.state
        obj.save()
        
        return JsonResponse({
            'success': True, 
            'state': obj.state, 
            'message': f"État changé avec succès: {'Actif' if obj.state else 'Inactif'}"
        })
    except ObjConnecte.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Objet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def refresh_state(request, id):
    """Actualise l'état de connexion d'un objet"""
    try:
        obj = ObjConnecte.objects.get(id=id)
        
        # Dans une application réelle, vous pourriez interroger l'état réel
        # via une API externe ou un service IoT
        # Pour l'exemple, on simule une mise à jour de connexion
        import random
        is_connected = random.choice([True, False])
        obj.connected = is_connected
        obj.save()
            
        return JsonResponse({
            'success': True,
            'state': obj.state,
            'connected': obj.connected,
            'message': 'État actualisé'
        })
    except ObjConnecte.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Objet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def delete_object(request, id):
    """Supprime un objet connecté"""
    try:
        obj = ObjConnecte.objects.get(id=id)
        # Vérification des permissions
        if request.user.xp_level != 'admin':
            return JsonResponse({'success': False, 'message': 'Seuls les administrateurs peuvent supprimer des objets'}, status=403)
        
        # Supprimer l'objet
        obj_name = obj.name
        obj.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f"L'objet {obj_name} a été supprimé avec succès"
        })
    except ObjConnecte.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Objet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)