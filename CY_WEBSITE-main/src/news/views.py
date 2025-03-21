from django.shortcuts import render

def index(request):
    return render(request,'news/index.html')

def article(request, number_article):
    #Ajouter la condition qui verifie si le numero de l'article est dispo 
    return render(request,f'news/article{number_article}')