from django.shortcuts import render, redirect
from django.db.models import Q
from .models import ObjConnecte, Type
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ObjConnecteForm  # Assume a form exists for ObjConnecte creation
from user.decorators import xp_level_required
from .models import Type
import os
from django.conf import settings
import json
import csv
from datetime import datetime, timedelta

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
        if request.user.xp_level not in ['complex', 'admin']:
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
def toggle_highlight(request, id):
    """Permet de marquer ou démarquer un objet connecté."""
    try:
        obj = ObjConnecte.objects.get(id=id)
        # Vérification des permissions
        if request.user.xp_level not in ['complex', 'admin']:
            return JsonResponse({'success': False, 'message': 'Permissions insuffisantes'}, status=403)
        
        # Changement de l'état "highlighted"
        obj.highlighted = not obj.highlighted
        obj.save()
        
        return JsonResponse({
            'success': True,
            'highlighted': obj.highlighted,
            'message': f"Objet {'marqué' if obj.highlighted else 'démarqué'} avec succès."
        })
    except ObjConnecte.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Objet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def delete_object(request, id):
    """Supprime un objet connecté (réservé aux administrateurs)."""
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
            'message': f"L'objet {obj_name} a été supprimé avec succès."
        })
    except ObjConnecte.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Objet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@xp_level_required('complex')
def create_object(request):
    """Permet aux utilisateurs de créer un objet connecté."""
    if request.method == 'POST':
        form = ObjConnecteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "L'objet connecté a été créé avec succès.")
            return redirect('objConnecte:objets')
    else:
        form = ObjConnecteForm()
    return render(request, 'objConnecte/create_object.html', {'form': form})

@xp_level_required('complex')
def edit_object(request, id):
    """Permet aux utilisateurs de modifier un objet connecté."""
    try:
        obj = ObjConnecte.objects.get(id=id)
    except ObjConnecte.DoesNotExist:
        messages.error(request, "Objet connecté introuvable.")
        return redirect('objConnecte:objets')

    old_image = obj.image.path if obj.image else None  # Save the path of the old image

    if request.method == 'POST':
        form = ObjConnecteForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            if 'image' in request.FILES and old_image:
                # Delete the old image file if a new one is uploaded
                if os.path.exists(old_image):
                    os.remove(old_image)
            form.save()
            messages.success(request, "L'objet connecté a été modifié avec succès.")
            return redirect('objConnecte:objets')
    else:
        form = ObjConnecteForm(instance=obj)

    return render(request, 'objConnecte/edit_object.html', {'form': form, 'objet': obj})

@login_required
@xp_level_required('complex')
@require_POST
def update_coordinates(request, id):
    """Update the latitude and longitude of an object."""
    try:
        obj = ObjConnecte.objects.get(id=id)
        data = json.loads(request.body)
        obj.latitude = data.get('latitude')
        obj.longitude = data.get('longitude')
        obj.save()
        return JsonResponse({'success': True, 'message': 'Coordonnées mises à jour avec succès.'})
    except ObjConnecte.DoesNotExist:
        return JsonResponse({'success': False, 'message': "L'objet n'existe pas."})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@xp_level_required('intermediate')
def object_reports(request, id=None):
    """Affiche les rapports d'utilisation pour un objet ou tous les objets"""
    # Paramètres de filtrage
    period = request.GET.get('period', 'day')
    report_type = request.GET.get('type', 'energy')
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        # Par défaut, 7 jours en arrière
        start_date = datetime.now() - timedelta(days=7)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_date = datetime.now()
    
    # Si un ID d'objet est fourni, afficher les rapports pour cet objet spécifique
    if id:
        try:
            obj = ObjConnecte.objects.get(id=id)
            objects = [obj]  # Liste contenant seulement cet objet
            single_object = True
        except ObjConnecte.DoesNotExist:
            messages.error(request, "Objet connecté introuvable.")
            return redirect('objConnecte:objets')
    else:
        # Sinon, afficher les rapports pour tous les objets
        objects = ObjConnecte.objects.all()
        single_object = False
        
        # Filtrage par type d'objet si spécifié
        type_id = request.GET.get('type_id', '')
        if type_id:
            objects = objects.filter(type_id=type_id)
    
    # Récupérer les données d'utilisation pour chaque objet
    reports_data = []
    total_consumption = 0
    
    for obj in objects:
        if report_type == 'energy':
            data = obj.get_energy_consumption(period)
            total_consumption += data['total']
            reports_data.append({
                'object': obj,
                'data': data
            })
    
    # Récupérer tous les types pour le filtre
    types = Type.objects.all()
    
    context = {
        'reports_data': reports_data,
        'total_consumption': round(total_consumption, 2),
        'period': period,
        'report_type': report_type,
        'single_object': single_object,
        'object_id': id,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'types': types,
        'selected_type_id': request.GET.get('type_id', ''),
    }
    
    return render(request, 'objConnecte/reports.html', context)

@login_required
@xp_level_required('intermediate')
def export_report(request, id=None, format='csv'):
    """Exporte les données d'utilisation au format CSV ou PDF"""
    period = request.GET.get('period', 'day')
    report_type = request.GET.get('type', 'energy')
    
    # Récupérer l'objet ou tous les objets
    if id:
        try:
            objects = [ObjConnecte.objects.get(id=id)]
        except ObjConnecte.DoesNotExist:
            messages.error(request, "Objet connecté introuvable.")
            return redirect('objConnecte:objets')
    else:
        objects = ObjConnecte.objects.all()
        
        # Filtrage par type d'objet si spécifié
        type_id = request.GET.get('type_id', '')
        if type_id:
            objects = objects.filter(type_id=type_id)
    
    # Si format est CSV
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="report_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Objet', 'Type', 'Date', 'Valeur', 'Unité'])
        
        for obj in objects:
            if report_type == 'energy':
                data = obj.get_energy_consumption(period)
                for entry in data['data']:
                    writer.writerow([
                        obj.name,
                        obj.type.name,
                        entry['date'].strftime("%Y-%m-%d %H:%M"),
                        entry['value'],
                        data['unit']
                    ])
        
        return response
    
    # Si format est JSON
    elif format == 'json':
        data = []
        
        for obj in objects:
            if report_type == 'energy':
                report_data = obj.get_energy_consumption(period)
                obj_data = {
                    'name': obj.name,
                    'type': obj.type.name,
                    'total': report_data['total'],
                    'unit': report_data['unit'],
                    'entries': []
                }
                
                for entry in report_data['data']:
                    obj_data['entries'].append({
                        'date': entry['date'].strftime("%Y-%m-%d %H:%M"),
                        'value': entry['value']
                    })
                
                data.append(obj_data)
        
        response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="report_{datetime.now().strftime("%Y%m%d")}.json"'
        return response
    
    else:
        messages.error(request, "Format d'exportation non supporté.")
        if id:
            return redirect('objConnecte:object_reports', id=id)
        else:
            return redirect('objConnecte:reports')