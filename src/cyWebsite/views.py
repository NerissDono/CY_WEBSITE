from django.shortcuts import render
from django.db.models import Q
from objConnecte.models import ObjConnecte, Type 
from news.models import Article, Category, Author

def index(request):
    list=[1,2,3]
    return render(request, 'cyWebsite/index.html', {'list': list})