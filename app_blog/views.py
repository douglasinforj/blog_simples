from django.shortcuts import render

def post_list(request):
    return render(request, 'app_blog/post_list.html')
