from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

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

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.email})"
