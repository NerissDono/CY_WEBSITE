from django import forms
from .models import ObjConnecte

class ObjConnecteForm(forms.ModelForm):
    class Meta:
        model = ObjConnecte
        fields = ['name', 'type', 'description', 'image', 'state', 'connected', 'ip', 'longitude', 'latitude']
