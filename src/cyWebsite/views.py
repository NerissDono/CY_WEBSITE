from django.shortcuts import render, redirect
from django.contrib.auth import logout
from news.models import Article

def index(request):
    articles = Article.objects.select_related('author').all()  # Fetch articles with their authors
    return render(request, 'cyWebsite/index.html', {'articles': articles})



