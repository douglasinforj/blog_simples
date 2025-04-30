from django.shortcuts import render
from . models import Post
from django.utils import timezone
from django.db.models import Q     #busca complexa


def post_list(request):

    query = request.GET.get('q', '')  #captura o termo da busca (ex: ?q=palavra), valor padrão vazio '' evita exibir 'None'
    
    posts = Post.objects.filter(published_date__lte=timezone.now())

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )

    
    posts = posts.order_by('published_date')

    return render(request, 'app_blog/post_list.html', {'posts': posts, 'query': query})
