from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from news.models import Author  # Importez le modèle Author

class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='data/profile_pictures/',
        blank=True,
        null=True,
        help_text="Téléchargez une image de profil (formats acceptés : JPEG, PNG)."
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Nom unique pour éviter les conflits
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Nom unique pour éviter les conflits
        blank=True
    )
    XP_LEVEL_CHOICES = [
        ('simple', 'Simple'),
        ('intermediate', 'Intermédiaire'),  # Nouveau niveau ajouté
        ('complex', 'Complexe'),
        ('admin', 'Admin'),
    ]
    xp_level = models.CharField(
        max_length=15,  # Augmentez la longueur pour inclure "intermediate"
        choices=XP_LEVEL_CHOICES,
        default='simple',
        verbose_name="Niveau d'XP"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.email})"

@receiver(post_save, sender=User)
def add_user_to_auth_group(sender, instance, **kwargs):
    if instance.xp_level in ['complex', 'admin']:
        # Ajoutez l'utilisateur au groupe "auth_user" ou créez un groupe spécifique
        group, created = Group.objects.get_or_create(name='Authors')
        instance.groups.add(group)
    else:
        # Supprimez l'utilisateur du groupe s'il n'est plus "complex" ou "admin"
        group = Group.objects.filter(name='Authors').first()
        if group:
            instance.groups.remove(group)

@receiver(post_save, sender=User)
def create_or_update_author(sender, instance, created, **kwargs):
    if instance.xp_level in ['complex', 'admin']:
        # Créez ou mettez à jour l'auteur associé
        Author.objects.update_or_create(
            name=instance.username,
            defaults={'email': instance.email}
        )
    elif not created:
        # Supprimez l'auteur si l'utilisateur n'est plus "complex" ou "admin"
        Author.objects.filter(name=instance.username).delete()
