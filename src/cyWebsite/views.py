from django.shortcuts import render, redirect
from django.contrib.auth import logout

def index(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    return render(request, 'cyWebsite/index.html')

def login(request):
    return render(request,'cyWebsite/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

