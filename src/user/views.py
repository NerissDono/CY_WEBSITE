from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfilePictureForm, CustomUpdateUserForm
from .models import User  # Utilisez votre modèle personnalisé


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Assurez-vous que 'index' correspond à une URL valide
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    form = CustomAuthenticationForm()
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
def update_user(request):
    if request.method == 'POST':
        form = CustomUpdateUserForm(request.POST,request.FILES , instance=request.user)
        if form.is_valid():
            print('yes')
            form.save()
            messages.success(request, "Vos informations de profil ont été mises à jour avec succès.")
            return redirect('news:visualisation')  # Redirigez vers la page de visualisation
    else:
        form = CustomUpdateUserForm(instance=request.user)
    return render(request, 'news/visualisation.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)  # Seuls les superutilisateurs peuvent modifier les niveaux d'XP
def update_user_xp_level(request, username, new_level):
    try:
        user = User.objects.get(username=username)
        user.xp_level = new_level
        user.save()
        messages.success(request, f"Le niveau d'XP de {username} a été mis à jour à '{new_level}'.")
    except User.DoesNotExist:
        messages.error(request, f"L'utilisateur '{username}' n'existe pas.")
    return redirect('admin:index')  # Redirigez vers l'interface d'administration ou une autre page appropriée
