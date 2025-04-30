from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    #rotas administrativas
    path('admin_blog/', views.painel_administrativo, name='painel_administrativo'),
    path('admin_blog/aprovar/<int:pk>/', views.aprovar_post, name='aprovar_post'),
    path('admin_blog/recusar/<int:pk>/', views.recusar_post, name='recusar_post'),
    path('admin_blog/excluir/<int:pk>/', views.excluir_post_admin, name='excluir_post_admin'),
    path('admin_blog/editar/<int:pk>/', views.editar_post_admin, name='editar_post_admin'),
]
