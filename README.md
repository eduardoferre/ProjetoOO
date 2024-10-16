# Projeto Django com MongoDB - `autodudu`

Este projeto é uma aplicação web desenvolvida em Django, utilizando o banco de dados MongoDB. Projeto na qual foi desenvolvido para conclusão da matéria Orientação a Objetos. Ele segue o padrão de arquitetura MVT (Model-View-Template) e inclui funcionalidades como gerenciamento de usuários, criação de anúncios, e uma interface amigável para navegação e edição de dados.

## Estrutura do Projeto

O projeto segue o padrão de arquitetura MVT do Django:

- **Model (M)**: Representa a camada de dados. A conexão com o MongoDB é feita usando o pacote `djongo`, permitindo a manipulação de objetos como automóveis, motos e anúncios.
- **View (V)**: Contém a lógica de controle e manipulação dos dados. As views são responsáveis por processar as solicitações HTTP e retornar as respostas apropriadas, seja para listar anúncios, criar ou editar registros.
- **Template (T)**: Define a interface do usuário. Utilizamos templates HTML com integração ao Bootstrap para garantir uma interface responsiva e amigável.

## Funcionalidades Principais

- **Gerenciamento de Automóveis e Motos**: Cadastro, edição e exclusão de automóveis e motos.
- **Criação de Anúncios**: Os usuários podem criar e gerenciar anúncios relacionados aos veículos cadastrados.
- **Interface de Login/Logout**: Sistema de autenticação para proteger páginas e recursos sensíveis.

## Tecnologias Utilizadas

- **Django**: Framework web Python.
- **MongoDB**: Banco de dados NoSQL utilizado para armazenar os dados da aplicação.
- **Docker**: Para conteinerização da aplicação e banco de dados.
- **Bootstrap 5**: Estilização dos templates e responsividade.
- **djongo**: Biblioteca para integrar Django com MongoDB.
  
## Pré-requisitos

- Docker e Docker Compose instalados.
- MongoDB instalado localmente ou em contêiner.
- Python 3.8+.

## Instalação e Configuração

1. Clone o repositório:

    ```bash
    git clone https://github.com/eduardoferre/ProjetoOO.git
    cd ProjetoOO
    ```

2. Pare o serviço MongoDB local (se necessário):

    ```bash
    sudo systemctl stop mongod
    ```
3. Construa e inicie o projeto usando Docker Compose:

    ```bash
    docker compose up --build -d
    ```

4. Acesse o contêiner do Django:

    ```bash
    docker exec -it autodudu_web /bin/bash
    ```

5. Execute as migrações para configurar o banco de dados:

    ```bash
    python manage.py migrate
    ```

6. Crie um superusuário para acessar o painel de administração:

    ```bash
    python manage.py createsuperuser
    ```

## Uso

### Painel Administrativo

Acesse o painel administrativo para gerenciar os dados diretamente no Django Admin. Ele pode ser acessado em:

[http://localhost:8000/admin](http://localhost:8000/admin)
