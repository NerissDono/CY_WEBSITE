from django import forms
from django.core.exceptions import ValidationError
from .models import Article, SiteAppearance

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'cover', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'article'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Contenu de l\'article'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if not title or not content:
            raise ValidationError("Le titre et le contenu sont obligatoires.")
        return cleaned_data

class SiteAppearanceForm(forms.ModelForm):
    class Meta:
        model = SiteAppearance
        fields = ['primary_color', 'font_family', 'enable_animations', 'site_title', 'footer_text']
        widgets = {
            'primary_color': forms.Select(attrs={'class': 'form-control'}),
            'font_family': forms.Select(attrs={'class': 'form-control'}),
            'enable_animations': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'site_title': forms.TextInput(attrs={'class': 'form-control'}),
            'footer_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'primary_color': 'Couleur principale',
            'font_family': 'Police d\'écriture',
            'enable_animations': 'Activer les animations',
            'site_title': 'Titre du site',
            'footer_text': 'Texte du pied de page',
        }
