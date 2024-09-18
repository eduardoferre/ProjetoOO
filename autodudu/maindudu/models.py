from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from djongo import models
from bson import ObjectId

class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)
    
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de email é obrigatório')
        email = self.normalize_email(email)  # Normaliza o email
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)  # Hash da senha
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(email, nome, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    _id = models.ObjectIdField(primary_key=True)
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UserManager()

    def __str__(self):
        return self.nome
    
    # Métodos para criar usuários
    @classmethod
    def create_user(cls, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de email é obrigatório')
        user = cls(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # Método para obter todos os usuários
    @classmethod
    def obter_todos_usuarios(cls):
        usuarios = Usuario.objects.values('_id', 'email', 'nome', 'is_active', 'is_staff')
        return usuarios
    
    def __str__(self):
        return f"{self.id} - {self.email}"  # Inclua o id junto com o email


class Automovel(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    ano = models.IntegerField()

    @classmethod
    def create_automovel(cls, marca, modelo, ano):
        if not marca or not modelo or not ano:
            raise ValueError("Todos os campos são obrigatórios")
        automovel = cls(marca=marca, modelo=modelo, ano=ano)
        automovel.save()
        return automovel

    @classmethod
    def obter_todos_automoveis(cls):
        return cls.objects.all()

    @classmethod
    def deletar_automovel(automovel_id):  # só pode deletar os administradores
        try:
            automovel = Automovel.objects.get(pk=ObjectId(automovel_id))
            automovel.delete()
        except Automovel.DoesNotExist:
            print(f"Automóvel com ID {automovel_id} não encontrado.")


class Carro(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    automovel = models.ForeignKey(Automovel, to_field='_id', on_delete=models.CASCADE)
    cor = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    numero_portas = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carros')  # Removendo o `to_field`

    def __str__(self):
        return f"{self.automovel.marca} - {self.tipo} ({self.cor})"
 
    @classmethod
    def create_carro(cls, automovel, cor, tipo, numero_portas, usuario_id):
        if not automovel or not cor or not tipo or not numero_portas:
            raise ValueError("Todos os campos são obrigatórios")
        carro = cls(automovel=automovel, cor=cor, tipo=tipo, numero_portas=numero_portas, usuario=usuario_id)
        carro.save()
        return carro
    
    @classmethod
    def obter_todos_carros(cls,user_id):
        return cls.objects.filter(usuario=ObjectId(user_id))
    
    @classmethod
    def deletar_carro(cls, carro_id):
        try:
            carro = Carro.objects.get(pk=ObjectId(carro_id))
            Anuncio.objects.filter(object_id=str(carro_id)).delete()
            carro.delete()
        except Carro.DoesNotExist:
            print(f"Carro com ID {carro_id} não encontrado.")


class Moto(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    automovel = models.ForeignKey(Automovel, on_delete=models.CASCADE)
    cilindradas = models.IntegerField()
    tipo = models.CharField(max_length=255)
    cor = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='motos')

    @classmethod
    def create_moto(cls, automovel, cilindradas, tipo, cor, usuario_id):
        if not automovel or not cilindradas or not tipo or not cor:
            raise ValueError("Todos os campos são obrigatórios")
        moto = cls(automovel=automovel, cilindradas=cilindradas, tipo=tipo, cor=cor, usuario=usuario_id)
        moto.save()
        return moto
    
    @classmethod
    def obter_todas_motos(cls, user_id):
        return cls.objects.filter(usuario=ObjectId(user_id))
        

    @classmethod
    def deletar_moto(cls, moto_id):
        try:
            moto = Moto.objects.get(pk=ObjectId(moto_id))
            Anuncio.objects.filter(object_id=str(moto_id)).delete()
            moto.delete()
        except Moto.DoesNotExist:
            print(f"Moto com ID {moto_id} não encontrado.")


class Anuncio(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=100)
    automovel = GenericForeignKey('content_type', 'object_id')
    preco_por_dia = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidade = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='anuncios_gerais')
    imagem = models.ImageField(upload_to='anuncios/', blank=True, null=True)  
   
    # Campo para descrição de texto
    descricao = models.TextField(blank=True, null=True)

    @classmethod
    def create_anuncio(cls, automovel, preco_por_dia, disponibilidade, usuario, descricao=None, imagem=imagem):
        if not automovel or not preco_por_dia or not disponibilidade or not usuario:
            raise ValueError("Todos os campos são obrigatórios")
        
        anuncio = cls(
            automovel=automovel, 
            preco_por_dia=preco_por_dia, 
            disponibilidade=disponibilidade, 
            usuario=usuario,
            descricao=descricao,
            imagem=imagem
        )
        anuncio.save()
        return anuncio
    
    @classmethod
    def obter_todos_anuncios(cls):
        return cls.objects.all()
    
    @classmethod
    def deletar_anuncio(cls, anuncio_id):
        try:
            anuncio = Anuncio.objects.get(pk=ObjectId(anuncio_id))
            anuncio.delete()
        except Anuncio.DoesNotExist:
            print(f"Anúncio com ID {anuncio_id} não encontrado.")

    @classmethod
    def obter_anuncios_usuario(cls, usuario_id):
        return cls.objects.filter(usuario=usuario_id)
    
    @classmethod
    def editar_anuncio(cls, anuncio_id, preco_por_dia, disponibilidade):
        try:
            anuncio = Anuncio.objects.get(pk=ObjectId(anuncio_id))
            anuncio.preco_por_dia = preco_por_dia
            anuncio.disponibilidade = disponibilidade
            anuncio.save()
        except Anuncio.DoesNotExist:
            print(f"Anúncio com ID {anuncio_id} não encontrado.")

    @classmethod
    def consulta_anuncioId(cls, anuncio_id):
        try:
            anuncio = Anuncio.objects.get(pk=ObjectId(anuncio_id))
            return anuncio
        except Anuncio.DoesNotExist:
            print(f"Anúncio com ID {anuncio_id} não encontrado.")

    @classmethod
    def obter_anuncios_usuario(cls, user_id):
        return cls.objects.filter(usuario=ObjectId(user_id))