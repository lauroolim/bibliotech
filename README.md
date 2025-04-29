# BiblioTech

Sistema de gerenciamento de biblioteca digital que permite catalogar, pesquisar e administrar acervos de livros e outros materiais bibliográficos.

## Tecnologias Utilizadas

- **Backend**: Node.js (Express)
- **Frontend**: EJS (Embedded JavaScript templates)
- **Banco de Dados**: PostgreSQL 15
- **Administração de DB**: pgAdmin 4
- **Containerização**: Docker e Docker Compose

## Configuração do Ambiente

### Pré-requisitos

- Docker e Docker Compose instalados
- Node.js (para desenvolvimento local)

### Iniciando o Projeto

1. Clone o repositório:

```bash
git clone [URL_DO_REPOSITORIO]
cd bibliotech
```

2. Instale as dependências:

```bash
npm install
```

3. Inicie os containers:

```bash
docker-compose up -d
```

4. Inicialize o banco de dados:

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

5. Inicie o sistema:

```bash
npm start
```

6. Acesse em <http://localhost:3000>

