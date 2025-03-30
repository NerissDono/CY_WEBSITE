from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from user.decorators import xp_level_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Article, Category, Author
from .forms import ArticleForm  # Importez le formulaire pour les articles

def accueil(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    return render(request, 'news/accueil.html')

def information(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    return render(request, 'news/information.html')

@login_required
@xp_level_required('complex')
def gestion(request):
    return render(request, 'news/gestion.html')

@user_passes_test(lambda u: u.is_superuser)
@xp_level_required('admin')
def administration(request):
    return render(request, 'news/administration.html')

@login_required
def visualisation(request):
    return render(request, "news/visualisation.html", {"user": request.user})

@login_required
def create_article(request):
    if request.user.xp_level not in ['complex', 'admin']:
        raise PermissionDenied("Vous n'avez pas les permissions nécessaires pour créer un article.")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            try:
                # Associez l'article à l'instance Author correspondante
                author = Author.objects.get(name=request.user.username)
                article.author = author
                article.save()  # Sauvegarde l'article dans la base de données
                messages.success(request, "L'article a été publié avec succès.")
                return redirect('news:visualisation')  # Redirigez vers la page de profil
            except Author.DoesNotExist:
                messages.error(request, "Vous n'êtes pas enregistré comme auteur.")
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Le formulaire contient des erreurs. Veuillez vérifier les champs.")
    else:
        form = ArticleForm()
    
    return render(request, 'news/create_article.html', {'form': form})

@login_required
def my_articles(request):
    try:
        # Récupérez l'auteur correspondant à l'utilisateur connecté
        author = Author.objects.get(name=request.user.username)
        # Récupérez les articles associés à cet auteur
        articles = Article.objects.filter(author=author)
    except Author.DoesNotExist:
        # Si l'utilisateur n'est pas un auteur, aucun article ne sera affiché
        articles = []
    return render(request, 'news/my_articles.html', {'articles': articles})

@login_required
def delete_article(request, article_id):
    try:
        # Récupérez l'article à supprimer
        article = Article.objects.get(id=article_id, author__name=request.user.username)
        if request.method == 'POST':
            article.delete()
            messages.success(request, "L'article a été supprimé avec succès.")
            return redirect('news:my_articles')
    except Article.DoesNotExist:
        messages.error(request, "L'article n'existe pas ou vous n'avez pas la permission de le supprimer.")
        return redirect('news:my_articles')
    return render(request, 'news/confirm_delete.html', {'article': article})

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


