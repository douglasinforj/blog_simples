from django.shortcuts import render
from . models import Post
from django.utils import timezone

def post_list(request):
    
    # Busca os posts com data de publicação menor ou igual à data e hora atual
    # e ordena do mais antigo para o mais recente
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'app_blog/post_list.html', {'posts': posts})
