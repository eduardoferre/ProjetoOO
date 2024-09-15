# Classe base Usuario
class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
    
    def editar_perfil(self, novo_nome, novo_email):
        self.nome = novo_nome
        self.email = novo_email


# Classe base Automóvel
class Automovel:
    def __init__(self, modelo, marca, ano, placa):
        self.modelo = modelo
        self.marca = marca
        self.ano = ano
        self.placa = placa

    def mostrar_info(self):
        return f"{self.marca} {self.modelo}, Ano: {self.ano}, Placa: {self.placa}"


# Subclasse Carro herda de Automóvel
class Carro(Automovel):
    def __init__(self, modelo, marca, ano, placa, num_portas):
        super().__init__(modelo, marca, ano, placa)
        self.num_portas = num_portas

    def mostrar_info(self):
        return f"Carro: {super().mostrar_info()}, Portas: {self.num_portas}"


# Subclasse Moto herda de Automóvel
class Moto(Automovel):
    def __init__(self, modelo, marca, ano, placa, cilindradas):
        super().__init__(modelo, marca, ano, placa)
        self.cilindradas = cilindradas

    def mostrar_info(self):
        return f"Moto: {super().mostrar_info()}, Cilindradas: {self.cilindradas}cc"


# Classe Anuncio que contém um Automóvel (composição)
class Anuncio:
    def __init__(self, automovel, preco_por_dia, disponibilidade=True):
        self.automovel = automovel  # Composição: um anúncio contém um automóvel (Carro ou Moto)
        self.preco_por_dia = preco_por_dia
        self.disponibilidade = disponibilidade

    def editar_anuncio(self, novo_preco, nova_disponibilidade):
        self.preco_por_dia = novo_preco
        self.disponibilidade = nova_disponibilidade

    def mostrar_anuncio(self):
        status = "Disponível" if self.disponibilidade else "Indisponível"
        return f"{self.automovel.mostrar_info()} - Preço por dia: R${self.preco_por_dia} - Status: {status}"


# Classe Cliente que pode criar anúncios
class Cliente(Usuario):
    def __init__(self, nome, email):
        super().__init__(nome, email)
        self.anuncios = []  # Agregação: cliente pode ter múltiplos anúncios
    
    def criar_anuncio(self, automovel, preco_por_dia):
        novo_anuncio = Anuncio(automovel, preco_por_dia)
        self.anuncios.append(novo_anuncio)

    def editar_anuncio(self, anuncio, novo_preco, nova_disponibilidade):
        if anuncio in self.anuncios:
            anuncio.editar_anuncio(novo_preco, nova_disponibilidade)

    def listar_anuncios(self):
        for anuncio in self.anuncios:
            print(anuncio.mostrar_anuncio())
