from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Utilisez votre modèle personnalisé

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'xp_level')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_picture', 'xp_level')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['profile_picture'].label = 'Photo de profil'
        return form
    


# Register your models here.
