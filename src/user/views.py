from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from .forms import ProfilePictureForm
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Assurez-vous que 'index' correspond à une URL valide
        else:
            messages.info(request, "Nom d'utilisateur ou mot de passe incorrect")
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('index')  # Assurez-vous que 'index' correspond à une URL valide

def register_user(request):
    if request.method == 'POST':
        form= CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('user:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Votre mot de passe a été changé avec succès.")
            return redirect('index')  # Redirect to a success page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})

def password_reset_request(request):

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='user/password_reset_email.html',
                subject_template_name='user/password_reset_subject.txt',
                use_https=request.is_secure(),
                from_email=settings.DEFAULT_FROM_EMAIL
            )
            messages.success(request, "Un e-mail de réinitialisation de mot de passe a été envoyé.")
            return redirect('user:login')
    else:
        form = PasswordResetForm()
    return render(request, 'user/password_reset.html', {'form': form})

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre photo de profil a été mise à jour avec succès.")
            return redirect('index')  # Redirigez vers une page appropriée
    else:
        form = ProfilePictureForm(instance=request.user)
    return render(request, 'user/update_profile_picture.html', {'form': form})
