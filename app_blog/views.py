from django.shortcuts import render, redirect
from . models import Post, Categoria
from django.utils import timezone
from django.db.models import Q     #busca complexa
from django.shortcuts import render, get_object_or_404 # retorna detalhes de um objeto especifico
from . forms import PostForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from taggit.models import Tag


def post_list(request):

    query = request.GET.get('q', '')  # captura o termo da busca (ex: ?q=palavra), valor padrão vazio '' evita exibir 'None'
    
    posts = Post.objects.filter(aprovado=True, published_date__lte=timezone.now())

    categorias = Categoria.objects.all()

    tags = Tag.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )

    
    posts = posts.order_by('-published_date')

    return render(request, 'app_blog/post_list.html', {'posts': posts, 'query': query, 'categorias': categorias,'tags': tags})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()  # SALVA AS TAGS e outros campos ManyToMany
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'app_blog/post_new.html', {'form': form, })


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # verifica se o usuário atual é o autor do post
    if post.author != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar este post.")
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()                                     # necessário para salvar as tags corretamente
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'app_blog/post_edit.html', {'form': form, 'post': post})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published_date__lte=timezone.now())  # para evitar que usuários vejam posts ainda não publicados.

    #contagem de visualizações
    post.visualizacoes += 1
    post.save(update_fields=['visualizacoes'])

    return render(request, 'app_blog/post_detail.html', {'post': post })


def lista_tags(request):
    tags = Tag.objects.all()
    return render(request, 'app_blog/lista_tags.html', {'tags': tags})


def posts_por_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag], aprovado=True)
    return render(request, 'app_blog/posts_por_tag.html', {'tag': tag, 'posts': posts})






#-----------------Administração do blog-----------------------

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def painel_administrativo(request):
    posts_pendentes = Post.objects.filter(aprovado=False, recusado=False)

    # Ultimos 10 posts aprovados para o gráfico
    posts_publicados = Post.objects.filter(aprovado=True).order_by('-published_date')[:10]

    context = {
        'posts_pendentes': posts_pendentes,
        'titles': [post.title for post in posts_publicados],
        'views': [post.visualizacoes for post in posts_publicados],
        'likes': [post.likes for post in posts_publicados],
        'dislikes': [post.dislikes for post in posts_publicados],
    }

    return render(request, 'app_blog/painel_admin.html',  context)




@user_passes_test(is_admin)
def aprovar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.aprovado = True
    post.published_date = timezone.now()
    post.save()
    return redirect('painel_administrativo')

@user_passes_test(is_admin)
def excluir_post_admin(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('painel_administrativo')

@user_passes_test(is_admin)
def recusar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.recusado = True
    post.save()
    return redirect('painel_administrativo')

@user_passes_test(is_admin)
def editar_post_admin(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('painel_administrativo')
    else:
        form = PostForm(instance=post)
    return render(request, 'app_blog/post_edit.html', {'form': form, 'post': post})



#-----------------------------Sistema de Likes-----------------------------

def votar(request, post_id, tipo):
    post = get_object_or_404(Post, id=post_id)
    cookie_key = f'post_voted_{post_id}'

    if request.COOKIES.get(cookie_key):
        return JsonResponse({'error': 'Você já votou.'}, status=403)

    if tipo == 'like':
        post.likes += 1
    elif tipo == 'dislike':
        post.dislikes += 1
    post.save()

    response = JsonResponse({
        'likes': post.likes,
        'dislikes': post.dislikes
    })
    response.set_cookie(cookie_key, 'true', max_age=60*60*24*30)  # 30 dias
    return response


#----------------Categorias---------------------

def explorar(request):
    categorias = Categoria.objects.all()
    return render(request, 'app_blog/explorar.html', {'categorias': categorias})

"""
def posts_por_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    posts = Post.objects.filter(categoria=categoria, aprovado=True).order_by('-published_date')
    return render(request, 'app_blog/post_list.html', {'posts': posts, 'categoria': categoria})
"""

def posts_por_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    posts = Post.objects.filter(categoria=categoria, aprovado=True).order_by('-published_date')
    tags = Tag.objects.all()
    categorias = Categoria.objects.all()  # adiciona todas as categorias
    return render(request, 'app_blog/post_list.html', {
        'posts': posts,
        'categoria': categoria,
        'categorias': categorias,
        'tags': tags
    })