from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test

def accueil(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    return render(request, 'news/accueil.html')

def information(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    return render(request, 'news/information.html')

@login_required
def gestion(request):
    return render(request, 'news/gestion.html')

@user_passes_test(lambda u: u.is_superuser)
def administration(request):
    return render(request, 'news/administration.html')

def visualisation(request):
    vehicules = [
        {
            "nom": "Peugeot 403 Rouge",
            "plaque": "AB-123-CD",
            "telephone": "06 11 22 33 44",
            "image": "vehicules/voiture1.png"
        },
        {
            "nom": "BMW M3 Grise",
            "plaque": "EF-456-GH",
            "telephone": "07 55 66 77 88",
            "image": "vehicules/voiture2.png"
        },
        {
            "nom": "Mercedes GLA Blanche",
            "plaque": "IJ-789-KL",
            "telephone": "06 98 76 54 32",
            "image": "vehicules/voiture3.png"
        },
        {
            "nom": "Mercedes GLE Grise",
            "plaque": "MN-321-OP",
            "telephone": "07 33 22 11 00",
            "image": "vehicules/voiture4.png"
        },
        {
            "nom": "Dacia Duster Blanche",
            "plaque": "QR-654-ST",
            "telephone": "06 70 80 90 10",
            "image": "vehicules/voiture5.png"
        },
    ]
    return render(request, "news/visualisation.html", {"vehicules": vehicules})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'news/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accueil')
    else:
        form = AuthenticationForm()
    return render(request, 'news/login.html', {'form': form})

def connexion(request):
    return render(request, 'news/connexion.html')


