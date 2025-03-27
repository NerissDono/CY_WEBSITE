from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

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
        help_texts = {
            'username': _('Obligatoire. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement.'),
            'email': _('Obligatoire. Entrez une adresse e-mail valide.'),
            'password1': _('Obligatoire. Au moins 8 caractères.'),
            'password2': _('Obligatoire. Entrez le même mot de passe que ci-dessus, pour vérification.'),
        }
        error_messages = {
            'username': {
                'unique': _("Ce nom d'utilisateur est déjà pris."),
            },
            'email': {
                'invalid': _("Entrez une adresse e-mail valide."),
            },
        }
        def save(self,commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user
           