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

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto com as variáveis do `.env.example`:


5. Inicie os containers:

```bash
docker-compose up -d
```

6. Inicialize o banco de dados:

```bash
# Acessar o bash do container PostgreSQL
docker exec -it bibliotech_db_1 bash

# Acessar o banco de dados com psql
psql -U admin -d bibliotech

# Copie e Cole o db.sql no terminal via psql
# db.sql:
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
...

# OBS.: Alguns comandos uteis do psql:
# \dt - Listar todas as tabelas
# \l - Listar todos os bancos de dados
# SELECT * FROM nome_tabela; - Visualizar registros de uma tabela
```

5. Execute a aplicação:

```bash
python app.py
```

6. Acesse em <http://localhost:5000>

