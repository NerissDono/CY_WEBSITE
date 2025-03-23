from django.contrib import admin
from .models import ObjConnecte, Type

@admin.register(ObjConnecte)
class ObjConnecteAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'date')
    list_filter = ('type', 'date')
    search_fields = ('name', 'description')
    date_hierarchy = 'date'
    ordering = ('date',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')