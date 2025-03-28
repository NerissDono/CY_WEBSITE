from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User  # Remplacez l'import par celui-ci

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

    def save(self,commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']
