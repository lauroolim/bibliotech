# BiblioTech

Sistema de gerenciamento de biblioteca digital que permite catalogar, pesquisar e administrar acervos de livros e outros materiais bibliográficos.

## Tecnologias Utilizadas

- **Backend**: Python (Flask)
- **Frontend**: HTML + Jinja2 (templates do Flask)
- **Banco de Dados**: PostgreSQL 15
- **Administração de DB**: pgAdmin 4
- **Containerização**: Docker e Docker Compose

## Configuração do Ambiente

### Pré-requisitos

- Python 3.10+ (para execução local)
- Docker e Docker Compose instalados

### Iniciando o Projeto

1. Clone o repositório:

```bash
git clone [URL_DO_REPOSITORIO]
cd bibliotech
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto com as variáveis do `.env.example`:


5. Inicie os containers:

```bash
docker-compose up --build -d
```

6. Inicialize o banco de dados:

```bash
# acessar o bash do container do app
$ docker exec -it app sh

# rode as migrations
$ python migrations.py
...

# comandos úteis para verificar o estado do banco de dados
# docker exec -it bibliotech bash -> para acessar o bash do container do banco de dados
# psql -U admin -d bibliotech -> para acessar o banco de dados
# \l -> para listar as tabelas
# \dt -> para listar os bancos de dados

```

7. Execute a aplicação:

```bash
python app.py
```

8. Acesse em <http://localhost:5000>

