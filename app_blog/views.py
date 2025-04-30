from django.shortcuts import render, redirect
from . models import Post
from django.utils import timezone
from django.db.models import Q     #busca complexa
from django.shortcuts import render, get_object_or_404 # retorna detalhes de um objeto especifico
from . forms import PostForm
from django.http import HttpResponseForbidden


def post_list(request):

    query = request.GET.get('q', '')  # captura o termo da busca (ex: ?q=palavra), valor padrão vazio '' evita exibir 'None'
    
    posts = Post.objects.filter(published_date__lte=timezone.now())

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )

    
    posts = posts.order_by('published_date')

    return render(request, 'app_blog/post_list.html', {'posts': posts, 'query': query})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'app_blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # verifica se o usuário atual é o autor do post
    if post.author != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar este post.")
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'app_blog/post_edit.html', {'form': form, 'post': post})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published_date__lte=timezone.now())  # para evitar que usuários vejam posts ainda não publicados.
    return render(request, 'app_blog/post_detail.html', {'post': post })
