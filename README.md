# Seazone TechTest

Projeto de backend para gestão de propriedades e reservas utilizando FastAPI, SQLAlchemy e PostgreSQL.

## Requisitos
- Python 3.10
- Docker (opcional, para ambiente containerizado)


## Índice
1. [Visão Geral](#visão-geral)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Execução do Projeto](#execução-do-projeto)
4. [Testes Automatizados](#testes-automatizados)
5. [Documentação e Links Úteis](#documentação-e-links-úteis)
6. [Exemplo de .env](#exemplo-de-env)

## Visão Geral
Este projeto é um sistema de reservas de propriedades, desenvolvido com Python 3.10, FastAPI, SQLAlchemy, Alembic e PostgreSQL. Inclui ambiente Docker, documentação, exemplos de uso e testes automatizados.

## Configuração do Ambiente
1. Clone o repositório:
	```bash
	git clone https://github.com/NeoThanatus/Seazone-TechTest.git
	cd Seazone-TechTest
	```
2. Crie e ative o ambiente virtual:
	```bash
	python3.10 -m venv venv
	source venv/bin/activate
	```
3. Instale as dependências:
	 ```bash
	 pip install -r requirements.txt
	 ```
4. Configure o arquivo `.env` conforme o exemplo em `.env.example`.

## Execução do Projeto
- Para rodar localmente:
	```bash
	uvicorn app.main:app --reload
	```
- Para rodar com Docker:
	```bash
	docker compose up --build
	```
- Para aplicar as migrações:
	```bash
	alembic upgrade head
	# ou via Docker
	docker-compose run --rm web alembic upgrade head
	```


## Testes Automatizados

Este projeto possui testes automatizados para garantir o funcionamento dos principais fluxos e regras de negócio.

### Tipos de Testes
- **Testes de Integração:** Validam endpoints da API, cenários de sucesso e erro, usando httpx e pytest-asyncio.
- **Testes Unitários:** Cobrem regras de negócio, como cálculo de valor, validação de datas e capacidade máxima.

### Estrutura dos Testes
Os testes estão localizados na pasta `tests/`:
- `test_properties.py`: Testes de propriedades.
- `test_reservations.py`: Testes de reservas.
- `test_integration_properties.py`: Testes de integração dos endpoints de propriedades.
- `test_integration_rap.py`: Testes de integração com exemplos de artistas do rap brasileiro.
- `test_unit_reservations.py`: Testes unitários das regras de negócio de reservas.

### Como Executar os Testes
Para rodar todos os testes:
```bash
pytest
```
Para rodar apenas testes unitários:
```bash
pytest tests/test_unit_reservations.py
```
Para rodar testes de integração:
```bash
pytest tests/test_integration_properties.py
pytest tests/test_integration_rap.py
```

### Resumo dos Testes Implementados
- Testes de integração cobrem cenários de criação, consulta, erro e validação dos endpoints principais.
- Testes unitários garantem o funcionamento das regras de negócio (cálculo de valor, datas, capacidade).
- Exemplos de dados reais e fictícios (artistas do rap brasileiro) foram usados para validar cenários diversos.
- Todos os testes podem ser executados via `pytest`, com cobertura dos principais fluxos do sistema.

## Exemplo de .env
Consulte o arquivo `.env.example` para configurar as variáveis de ambiente necessárias.

---


## Observações
- Para produção, remova o parâmetro `--reload` do Uvicorn.
- As variáveis do banco podem ser ajustadas conforme o ambiente.
- O projeto está pronto para deploy em Docker ou execução local.

---

## Documentação e Links Úteis
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [pytest](https://docs.pytest.org/)
- [httpx](https://www.python-httpx.org/)
- [Docker](https://docs.docker.com/)


Se tiver dúvidas, consulte a documentação dos endpoints via Swagger ou Redoc.

---


## Exemplos de Entrada, Saída e URLs

### Criar Reserva (POST)
**URL:**
```
POST /reservations/
```
**Exemplo de corpo da requisição:**
```json
{
	"property_id": 1,
	"guest_name": "Mano Brown",
	"check_in": "2025-09-01",
	"check_out": "2025-09-05",
	"guests": 2
}
```
**Exemplo de resposta:**
```json
{
	"id": 10,
	"property_id": 1,
	"guest_name": "Mano Brown",
	"check_in": "2025-09-01",
	"check_out": "2025-09-05",
	"guests": 2,
	"total_price": 2000.0
}
```

### Consultar Reserva (GET)
**URL:**
```
GET /reservations/10
```
**Exemplo de resposta:**
```json
{
	"id": 10,
	"property_id": 1,
	"guest_name": "Mano Brown",
	"check_in": "2025-09-01",
	"check_out": "2025-09-05",
	"guests": 2,
	"total_price": 2000.0
}
```

### Exemplo de erro (saída)
**URL:**
```
POST /reservations/
```
**Exemplo de corpo da requisição:**
```json
{
	"property_id": 1,
	"guest_name": "Emicida",
	"check_in": "2025-09-01",
	"check_out": "2025-09-05",
	"guests": 20
}
```
**Exemplo de resposta de erro:**
```json
{
	"detail": "Capacidade máxima excedida para esta propriedade."
}
```
