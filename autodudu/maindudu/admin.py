from django.contrib import admin
from .models import Usuario, Automovel, Carro, Moto, Anuncio

# Registrar o modelo de usuário no admin
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'is_active', 'is_staff')
    search_fields = ('email', 'nome')

# Registrar outros modelos no admin
@admin.register(Automovel)
class AutomovelAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ano')
    search_fields = ('marca', 'modelo')

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ('automovel', 'cor', 'tipo', 'numero_portas', 'usuario')
    search_fields = ('automovel__marca', 'automovel__modelo', 'cor')

@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ('automovel', 'cilindradas', 'tipo', 'cor', 'usuario')
    search_fields = ('automovel__marca', 'automovel__modelo', 'tipo')

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('automovel', 'preco_por_dia', 'disponibilidade', 'usuario')
    search_fields = ('automovel__marca', 'automovel__modelo', 'preco_por_dia')
