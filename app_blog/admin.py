from django.contrib import admin
from django.utils import timezone
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date', 'is_published','likes', 'dislikes', 'aprovado', 'recusado')
    list_filter = ('author', 'published_date', 'created_date', 'aprovado', 'recusado')
    search_fields = ('title', 'text', 'author__username')
    readonly_fields = ('created_date', 'published_date', 'likes', 'dislikes')
    actions = ['publicar_posts', 'despublicar_posts', 'aprovar_posts', 'recusar_posts']

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'text', 'aprovado', 'recusado', 'likes', 'dislikes')
        }),
        ('Publicação', {
            'fields': ('created_date', 'published_date'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(boolean=True, description="Publicado?")
    def is_published(self, obj):
        return obj.published_date is not None

    def publicar_posts(self, request, queryset):
        count = queryset.update(published_date=timezone.now())
        self.message_user(request, f"{count} post(s) publicado(s) com sucesso.")
    publicar_posts.short_description = "Publicar posts selecionados"

    def despublicar_posts(self, request, queryset):
        count = queryset.update(published_date=None)
        self.message_user(request, f"{count} post(s) despublicado(s) com sucesso.")
    despublicar_posts.short_description = "Despublicar posts selecionados"

    def aprovar_posts(self, request, queryset):
        count = queryset.update(aprovado=True, recusado=False)
        self.message_user(request, f"{count} post(s) aprovado(s) com sucesso.")
    aprovar_posts.short_description = "Aprovar posts selecionados"

    def recusar_posts(self, request, queryset):
        count = queryset.update(recusado=True, aprovado=False)
        self.message_user(request, f"{count} post(s) recusado(s) com sucesso.")
    recusar_posts.short_description = "Recusar posts selecionados"