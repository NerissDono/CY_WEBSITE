from django.contrib import admin
from .models import Article, Author, Category, Comment, SiteAppearance


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')
    readonly_fields = ('image_preview',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('name', 'email')

@admin.register(SiteAppearance)
class SiteAppearanceAdmin(admin.ModelAdmin):
    list_display = ('primary_color', 'font_family', 'site_title', 'enable_animations')
    
    def has_add_permission(self, request):
        # Empêcher la création de plusieurs instances
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

