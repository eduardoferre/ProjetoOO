# urls.py (dentro da pasta maindudu)
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
    path('automoveis/criar/', views.criar_automovel, name='criar_automovel'),
    path('automoveis/', views.listar_automoveis, name='listar_automoveis'),
    path('carro/criar/', views.criar_carro, name='criar_carro'),
    path('carro/listar/', views.listar_carros, name='listar_carros'),
    path('carro/deletar/<str:carro_id>/', views.deletar_carro, name='deletar_carro'),
    path('moto/criar/', views.criar_moto, name='criar_moto'),
    path('moto/listar/', views.listar_motos, name='listar_motos'),
    path('moto/deletar/<str:moto_id>/', views.deletar_moto, name='deletar_moto'),
    path('anuncio/listar/', views.listar_anuncios, name='listar_anuncios'),
    path('anuncio/criar/', views.criar_anuncio, name='criar_anuncio'),
    path('anuncio/editar/<str:anuncio_id>/', views.editar_anuncio, name='editar_anuncio'),
    path('anuncio/deletar/<str:anuncio_id>/', views.deletar_anuncio, name='deletar_anuncio'),
    path('anuncio/consulta/<str:anuncio_id>/', views.consulta_anuncio, name='consulta_anuncio'),
    path('meus-anuncios/', views.meus_anuncios, name='meus_anuncios'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]