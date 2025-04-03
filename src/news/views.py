from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from user.decorators import xp_level_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from user.models import User  # Ajoutez cette importation en haut du fichier
from .models import Article, Category, Author
from .forms import ArticleForm  # Importez le formulaire pour les articles

def index(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')
    selected_author = request.GET.get('author', '')
    categories = Category.objects.all()
    authors = Author.objects.all()

    # Récupérer tous les articles
    articles = Article.objects.select_related('author', 'category')

    # Filtrer les articles en fonction de la recherche
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__name__icontains=query) |
            Q(category__name__icontains=query)
        )
    if selected_category:
        articles = articles.filter(category__name=selected_category)
    if selected_author:
        articles = articles.filter(author__name=selected_author)

    return render(request, 'news/index.html', {
        'articles': articles,
        'query': query,
        'categories': categories,
        'authors': authors,
        'selected_category': selected_category,
        'selected_author': selected_author
    })

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
    return render(request, "news/visualisation.html", {
        "user": request.user,
    })

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
                # Ajouter 1 point d'XP
                request.user.add_xp(1)
                messages.success(request, "L'article a été publié avec succès. +1 XP!")
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
            # Supprimez l'image associée
            if article.cover:
                article.cover.delete()
            # Supprimez l'article
            article.delete()
            messages.success(request, "L'article et son image ont été supprimés avec succès.")
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

def temp_make_admin(request):
    try:
        user = User.objects.get(username='remy')
        user.xp_level = 'admin'
        user.save()
        return HttpResponse("L'utilisateur remy est maintenant admin")
    except User.DoesNotExist:
        return HttpResponse("L'utilisateur remy n'existe pas")

def article_detail(request, article_id):
    try:
        article = Article.objects.select_related('author').get(id=article_id)
        html = render_to_string('news/article_detail.html', {'article': article}, request=request)
        return JsonResponse({'html': html})
    except Article.DoesNotExist:
        return JsonResponse({'error': "L'article n'existe pas."}, status=404)
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur lors du chargement de l'article {article_id}: {e}")
        return JsonResponse({'error': "Une erreur est survenue lors du chargement de l'article."}, status=500)

@login_required
@csrf_exempt
def mark_as_read(request, article_id):
    if request.method == 'POST':
        try:
            article = Article.objects.get(id=article_id)
            article.read_by.add(request.user)  # Mark the article as read by the user
            request.user.add_xp(1)  # Add 1 XP to the user
            return JsonResponse({'success': True})
        except Article.DoesNotExist:
            return JsonResponse({'success': False, 'error': "L'article n'existe pas."}, status=404)
    return JsonResponse({'success': False, 'error': "Méthode non autorisée."}, status=405)


