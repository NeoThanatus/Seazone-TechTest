# Seazone TechTest

Projeto de backend para gestão de propriedades e reservas utilizando FastAPI, SQLAlchemy e PostgreSQL.

## Requisitos
- Python 3.10
- Docker (opcional, para ambiente containerizado)

## Instalação

```bash
# Clone o repositório
$ git clone https://github.com/NeoThanatus/Seazone-TechTest
$ cd Seazone-TechTest

# Crie e ative o ambiente virtual
$ python3.10 -m venv .venv
$ source .venv/bin/activate

# Instale as dependências
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

## Configuração do ambiente
Crie um arquivo `.env` na raiz do projeto com base no exemplo abaixo:

### .env.example
```
DATABASE_URL=postgresql+asyncpg://seazone_user:seazone_pass@localhost:5432/seazone
DATABASE_KEY=
SYNC_DATABASE_URL=postgresql://seazone_user:seazone_pass@localhost:5432/seazone
```

## Executando o projeto

### Local
```bash
$ uvicorn app.main:app --reload
```

### Docker
```bash
$ docker-compose up --build
```

## Endpoints
- API: [http://localhost:8000](http://localhost:8000)
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Migrações de banco de dados
```bash
# Executar migrações Alembic
$ alembic upgrade head
```

## Estrutura do projeto
- `app/` - Código fonte principal
- `alembic/` - Migrações do banco de dados
- `requirements.txt` - Dependências
- `Dockerfile` e `docker-compose.yml` - Ambiente containerizado

## Testes
Adicione seus testes em uma pasta `tests/` e utilize pytest para rodar:
```bash
$ pytest
```

## Observações
- Para produção, remova o parâmetro `--reload` do Uvicorn.
- As variáveis do banco podem ser ajustadas conforme o ambiente.
- O projeto está pronto para deploy em Docker ou execução local.

---

## Documentação oficial
- [FastAPI](https://fastapi.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Docker](https://docs.docker.com/)
- [PostgreSQL](https://www.postgresql.org/docs/)
 - [Pydantic](https://docs.pydantic.dev/latest/)
 - [Uvicorn](https://www.uvicorn.org/)

Se tiver dúvidas, consulte a documentação dos endpoints via Swagger ou Redoc.
