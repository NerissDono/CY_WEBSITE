from django.shortcuts import render
from .models import ObjConnecte

def index(request):
    return render(request, 'objConnecte/index.html')

def objets(request):

    objets = ObjConnecte.objects.all()

    return render(request, 'objConnecte/objets.html', {'objets': objets})

def objet(request, id):
    
    objet = ObjConnecte.objects.get(id=id)

    return render(request, 'objConnecte/objet.html', {'objet': objet})


