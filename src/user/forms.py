from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User  # Utilisez votre modèle personnalisé
from .func import send_verification_email

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_("Adresse e-mail"))

    class Meta:
        model = User  
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _('Nom d\'utilisateur'),
            'email': _('Adresse e-mail'),
            'password1': _('Mot de passe'),
            'password2': _('Confirmer le mot de passe'),
        }
        error_messages = {
            'username': {
                'unique': _("Ce nom d'utilisateur est déjà pris."),
            },
            'email': {
                'invalid': _("Entrez une adresse e-mail valide."),
            },
        }
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False  # Désactiver le compte jusqu'à la validation
        if commit:
            user.save()
            send_verification_email(user, self.request)  # Envoyer l'email de validation
        return user

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CustomUpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_naissance', 'profile_picture']
        labels = {
            'username': _('Nom d\'utilisateur'),
            'email': _('Adresse e-mail'),
            'first_name': _('Prénom'),
            'last_name': _('Nom de famille'),
            'date_naissance': _('Date de naissance'),
            'profile_picture': _('Photo de profil'),
        }
        error_messages = {
            'username': {
                'unique': _("Ce nom d'utilisateur est déjà pris."),
            },
            'email': {
                'invalid': _("Entrez une adresse e-mail valide."),
            },
        }
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        profile_picture = cleaned_data.get('profile_picture')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Cette adresse e-mail est déjà utilisée."))
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
