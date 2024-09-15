from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django import forms
from maindudu.models import Automovel, Carro, Moto, Anuncio
from django.shortcuts import render, redirect, get_object_or_404
from bson import ObjectId
from django.contrib.auth.decorators import login_required



Usuario = get_user_model()

# Formulário de Registro
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'password']

# View para registrar o usuário
def register(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Use o método create_user para garantir que o usuário seja criado corretamente
            Usuario.create_user(
                email=form.cleaned_data['email'],
                nome=form.cleaned_data['nome'],
                password=form.cleaned_data['password']
            )
            return redirect('listar_usuarios')  # Nome da URL que lista os usuários
    else:
        form = UsuarioForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('listar_usuarios')  # Substitua 'home' pela sua URL de redirecionamento pós-login
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def listar_usuarios(request):
    if request.method == 'GET':
        usuarios = Usuario.obter_todos_usuarios()
        return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

@login_required
def listar_automoveis(request):
    automoveis = Automovel().obter_todos_automoveis()  # Chamando o método do model
    return render(request, 'listar_automoveis.html', {'automoveis': automoveis})

# Formulário para Automóvel
class AutomovelForm(forms.ModelForm):
    class Meta:
        model = Automovel
        fields = ['marca', 'modelo', 'ano']  # Campos do modelo Automovel

@login_required
def criar_automovel(request):
    if request.method == 'POST':
        form = AutomovelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_automoveis')
    else:
        form = AutomovelForm()
    
    return render(request, 'criar_automovel.html', {'form': form})



@login_required
def criar_carro(request):
    if request.method == 'POST':
        automovel_id = request.POST.get('automovel')       
        automovel = Automovel.objects.get(pk=ObjectId(automovel_id))
        cor = request.POST.get('cor')
        tipo = request.POST.get('tipo')
        numero_portas = request.POST.get('numero_portas')
        usuario = request.user
        Carro.create_carro(automovel, cor, tipo, numero_portas, usuario)
        return redirect('listar_carros')
    else:
        automoveis = Automovel.obter_todos_automoveis()  # Obter automóveis disponíveis
        return render(request, 'criar_carro.html', {'automoveis': automoveis})

@login_required
def listar_carros(request):
    user_id = request.user.pk
    carros = Carro.obter_todos_carros(user_id)
    return render(request, 'listar_carros.html', {'carros': carros})

@login_required
def deletar_carro(request, carro_id): # REFAZER <<<<<<<<< SOMENTE O USUARIO QUE CRIOU PODE DELETAR
    Carro.deletar_carro(carro_id)
    return redirect('listar_carros')

@login_required
def criar_moto(request):
    if request.method == 'POST':
        automovel_id = request.POST.get('automovel')
        automovel = Automovel.objects.get(pk=ObjectId(automovel_id))
        cilindradas = request.POST.get('cilindradas')
        tipo = request.POST.get('tipo')
        cor = request.POST.get('cor')
        usuario = request.user
        Moto.create_moto(automovel, cilindradas, tipo, cor, usuario)
        return redirect('listar_motos')
    else:
        automoveis = Automovel.obter_todos_automoveis()  # Obter automóveis disponíveis
        return render(request, 'criar_moto.html', {'automoveis': automoveis})

@login_required
def listar_motos(request):
    user_id = request.user.pk
    motos = Moto.obter_todas_motos(user_id)
    return render(request, 'listar_motos.html', {'motos': motos})

@login_required
def deletar_moto(request, moto_id): # COLOCAR PRA DELETAR APENAS O USER RESPONSÁVEL
    Moto.deletar_moto(moto_id)
    return redirect('listar_motos')

# View para listar todos os anúncios
def listar_anuncios(request):
    anuncios = Anuncio.obter_todos_anuncios()
    return render(request, 'listar_anuncios.html', {'anuncios': anuncios})

@login_required
def criar_anuncio(request):
    if request.method == 'POST':
        preco_por_dia = request.POST.get('preco_por_dia')
        disponibilidade = request.POST.get('disponibilidade') == 'on'
        descricao = request.POST.get('descricao')
        usuario = request.user
        
        automovel_id = request.POST.get('automovel')  # Recebe o ID do automóvel
        automovel_tipo = request.POST.get('automovel_tipo')  # Pode ser 'carro' ou 'moto'
        
        if automovel_tipo == 'carro':
            automovel = Carro.objects.get(pk=ObjectId(automovel_id))
        elif automovel_tipo == 'moto':
            automovel = Moto.objects.get(pk=ObjectId(automovel_id))
        
        if preco_por_dia and disponibilidade and usuario and automovel:
            Anuncio.create_anuncio(automovel, preco_por_dia, disponibilidade, usuario, descricao)
            return redirect('listar_anuncios')
        
    carros = Carro.obter_todos_carros(request.user.pk)
    motos = Moto.obter_todas_motos(request.user.pk)
    
    return render(request, 'criar_anuncio.html', {'carros': carros, 'motos': motos})

@login_required
def editar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, pk=ObjectId(anuncio_id))
    if request.method == 'POST':
        anuncio.preco_por_dia = request.POST.get('preco_por_dia')
        anuncio.disponibilidade = request.POST.get('disponibilidade')
        anuncio.save()
        return redirect('listar_anuncios')
    return render(request, 'editar_anuncio.html', {'anuncio': anuncio})

@login_required
def deletar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, pk=ObjectId(anuncio_id))
    if request.method == 'POST':
        anuncio.delete()
        return redirect('listar_anuncios')
    return render(request, 'deletar_anuncio.html', {'anuncio': anuncio})

# View para consultar um anúncio por ID
def consulta_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, pk=ObjectId(anuncio_id))
    return render(request, 'consulta_anuncio.html', {'anuncio': anuncio})

@login_required
def meus_anuncios(request):
    # Obtém os anúncios do usuário logado
    user_id = request.user.pk
    anuncios = Anuncio.obter_anuncios_usuario(user_id)
    
    # Renderiza a página com os anúncios do usuário
    return render(request, 'meus_anuncios.html', {'anuncios': anuncios})