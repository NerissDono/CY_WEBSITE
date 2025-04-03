from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import User

@receiver(user_logged_in)
def increment_login_count(sender, request, user, **kwargs):
    if isinstance(user, User):
        user.login_count += 1  # Increment login count
        user.add_xp(1)  # Add 1 XP
