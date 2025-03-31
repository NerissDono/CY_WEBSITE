from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfilePictureForm, CustomUpdateUserForm
from .models import User  # Utilisez votre modèle personnalisé
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User

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
            user = form.save(commit=False)
            user.is_active = False  # Désactiver le compte jusqu'à ce que l'utilisateur confirme son email
            user.save()
            send_verification_email(user, request)
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
        form = CustomUpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos informations de profil ont été mises à jour avec succès.")
            return redirect('news:visualisation')
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour de vos informations. Veuillez vérifier les champs.")
    else:
        form = CustomUpdateUserForm(instance=request.user)
    return render(request, 'news/visualisation.html', {'form': form, 'user': request.user})

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']
        user = request.user
        user.profile_picture = profile_picture
        user.save()
        messages.success(request, "Votre photo de profil a été mise à jour avec succès.")
    else:
        messages.error(request, "Une erreur est survenue lors de la mise à jour de votre photo de profil.")
    return redirect('news:visualisation')

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

@login_required
def search_user(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).exclude(id=request.user.id).values('username', 'email', 'profile_picture')
        results = list(users)
        for user in results:
            if user['profile_picture']:
                user['profile_picture'] = request.build_absolute_uri(settings.MEDIA_URL + user['profile_picture'])
            else:
                user['profile_picture'] = request.build_absolute_uri(settings.STATIC_URL + 'default_profile.png')
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

@login_required
def public_profile(request, username):
    try:
        user = User.objects.get(username=username)
        return render(request, 'user/public_profile_modal.html', {
            'user_profile': user
        })
    except User.DoesNotExist:
        return JsonResponse({'error': "L'utilisateur demandé n'existe pas."}, status=404)

def send_verification_email(user, request):
    current_site = get_current_site(request)
    subject = 'Confirmez votre inscription'
    message = render_to_string('user/verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject, message, None, [user.email])

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter.")
        return redirect('user:login')  
    else:
        return HttpResponse('Le lien d\'activation est invalide.')
