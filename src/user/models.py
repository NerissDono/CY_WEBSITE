from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.apps import apps

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
    date_naissance = models.DateField(
        blank=True,
        null=True,
        help_text="Entrez votre date de naissance (format : DD-MM-YYYY)."
    )
    xp_points = models.IntegerField(default=0)
    login_count = models.IntegerField(default=0, help_text="Nombre de connexions de l'utilisateur.")
    
    def pourcentage_xp(self):
        return int((self.xp_points / 10) * 100)

    def add_xp(self, points):
        self.xp_points += points
        if self.xp_points >= 10:
            if self.xp_level == 'simple':
                self.xp_level = 'intermediate'
            elif self.xp_level == 'intermediate':
                self.xp_level = 'complex'
            elif self.xp_level == 'complex':
                self.xp_level = 'admin'
            self.xp_points = 0  # Reset XP points after leveling up
        if self.xp_level == 'admin':  # Cap XP at 10/10 for admins
            self.xp_points = min(self.xp_points, 10)
        self.save()

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
    Author = apps.get_model('news', 'Author')  # Déplacez ici
    Article = apps.get_model('news', 'Article')  # Déplacez ici
    if instance.xp_level in ['complex', 'admin']:
        # Créez ou mettez à jour l'auteur associé
        Author.objects.update_or_create(
            name=instance.username,
            defaults={'email': instance.email}
        )
    elif not created:
        # Vérifiez si des articles existent avant de supprimer l'auteur
        if not Article.objects.filter(author__name=instance.username).exists():
            Author.objects.filter(name=instance.username).delete()
        else:
            # Logique alternative si des articles existent
            pass

@receiver(post_save, sender=User)
def sync_admin_rights(sender, instance, **kwargs):
    """
    Synchronise les droits d'administration (is_staff et is_superuser)
    en fonction du niveau d'XP de l'utilisateur.
    """
    if instance.xp_level == 'admin':
        if not instance.is_staff or not instance.is_superuser:
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()
    else:
        if instance.is_staff or instance.is_superuser:
            instance.is_staff = False
            instance.is_superuser = False
            instance.save()

class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
