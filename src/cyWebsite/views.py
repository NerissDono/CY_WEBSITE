from django.shortcuts import render, redirect
from django.contrib.auth import logout

def index(request):
    return render(request, 'cyWebsite/index.html')



