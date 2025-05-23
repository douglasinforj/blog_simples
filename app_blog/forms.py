from django import forms 
from .models import Post
from taggit.forms import TagField, TagWidget

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'video_url', 'categoria', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do post',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o conteúdo do post',
                'rows': 6,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control', 'placeholder': 'https://youtube.com/...'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control',
            }),
            'tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Digite tags separadas por vírgula (ex: viagem, comida, verão)'
        }),
        }
        labels = {
            'title': 'Título',
            'text': 'Conteúdo',
            'image': 'Imagem',
            'video_url': 'Link do vídeo do YouTube', 
            'categoria': 'Categoria',
            'tags': 'Tags',
        }
        