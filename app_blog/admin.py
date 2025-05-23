from django.contrib import admin
from django.utils import timezone
from .models import Post, Categoria
from django.utils.html import format_html

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    #mostra as tags na list_display
    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = "Tags"

    list_display = ('title', 'author', 'categoria','get_tags','created_date', 'published_date', 'is_published','likes', 'dislikes', 'aprovado', 'recusado')
    list_filter = ('author', 'categoria' ,'published_date', 'created_date', 'aprovado', 'recusado')
    search_fields = ('title', 'text', 'author__username', 'categoria__nome', 'tags__name')
    readonly_fields = ('created_date', 'published_date', 'likes', 'dislikes', 'image_preview')
    actions = ['publicar_posts', 'despublicar_posts', 'aprovar_posts', 'recusar_posts']

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'categoria','text', 'image', 'tags','image_preview','aprovado', 'recusado', 'likes', 'dislikes')
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


    #Função para exibir miniatura da imagem no admin:
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" style="object-fit:cover;" />', obj.image.url)
        return "(Sem imagem)"
    image_preview.short_description = "Pré-visualização da imagem"



@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)