from django.core.management.base import BaseCommand
from user.models import User
from news.models import Author

class Command(BaseCommand):
    help = "Synchronise les utilisateurs avec un niveau d'XP 'complex' ou 'admin' avec la base des auteurs."

    def handle(self, *args, **kwargs):
        users = User.objects.filter(xp_level__in=['complex', 'admin'])
        for user in users:
            Author.objects.update_or_create(
                name=user.username,
                defaults={'email': user.email}
            )
        self.stdout.write(self.style.SUCCESS("Synchronisation des auteurs terminée."))
