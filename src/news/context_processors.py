from .models import SiteAppearance
from django.db.utils import OperationalError, ProgrammingError

def site_appearance(request):
    """
    Ajoute les paramètres d'apparence du site à tous les templates
    Gère le cas où la table n'existe pas encore
    """
    try:
        return {
            'site_appearance': SiteAppearance.get_current()
        }
    except (OperationalError, ProgrammingError):
        # Utiliser des valeurs par défaut si la table n'existe pas encore
        class DefaultAppearance:
            primary_color = '#1e2a47'
            font_family = 'Roboto, sans-serif'
            enable_animations = True
            site_title = 'StarCity'
            footer_text = '© 2025 CY_WEBSITE. Tous droits réservés.'
        
        return {
            'site_appearance': DefaultAppearance()
        }
