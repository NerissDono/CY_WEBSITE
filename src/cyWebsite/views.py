from django.shortcuts import render
from django.db.models import Q
from news.models import Article, Category, Author

def index(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')
    selected_author = request.GET.get('author', '')
    categories = Category.objects.all()
    authors = Author.objects.all()

    articles = Article.objects.select_related('author', 'category')

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )
    if selected_category:
        articles = articles.filter(category__name=selected_category)
    if selected_author:
        articles = articles.filter(author__name=selected_author)

    return render(request, 'cyWebsite/index.html', {
        'articles': articles,
        'query': query,
        'categories': categories,
        'authors': authors,
        'selected_category': selected_category,
        'selected_author': selected_author
    })



