from django.shortcuts import render

def index(request):
    return render(request,'cyWebsite/index.html')

def login(request):
    return render(request,'cyWebsite/login.html')

