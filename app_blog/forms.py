from django import forms 
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
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
        }
        labels = {
            'title': 'Título',
            'text': 'Conteúdo',
            'image': 'Imagem'
        }
        