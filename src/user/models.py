from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='data/profile_pictures/', blank=True, null=True)
    date_joined = models.DateTimeField(default=datetime.now)
    last_login = models.DateTimeField(auto_now=True)
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

    def __str__(self):
        return self.username
    
    def authenticate(self, request, username=None, password=None):
        try:
            user = self.get(username=username)
            if user.check_password(password):
                return user
        except self.DoesNotExist:
            return None
        return None
