# Docker Compose Setup - FastAPI com PostgreSQL

## Configuração Inicial

### 1. Criar arquivo `.env`

Copie o `.env.example` para `.env`:

```bash
cp .env.example .env
```

### 2. Instalar dependências

```bash
uv sync
```

### 3. Iniciar PostgreSQL com Docker Compose

```bash
docker-compose up -d
```

### 4. Verificar a conexão

```bash
# PostgreSQL estará disponível em: localhost:5432
# Usuário: fastapi_user
# Senha: fastapi_password
# Banco de dados: fastapi_db
```

## Comandos Úteis

### Parar o PostgreSQL

```bash
docker-compose down
```

### Parar e remover volumes (limpar dados)

```bash
docker-compose down -v
```

### Ver logs do PostgreSQL

```bash
docker-compose logs -f postgres
```

### Acessar o PostgreSQL diretamente

```bash
docker-compose exec postgres psql -U fastapi_user -d fastapi_db
```

## Variáveis de Ambiente

A URL de conexão está configurada em `.env`:

```
DATABASE_URL=postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_db
```

## Dependências Atualizadas

- `asyncpg`: Driver PostgreSQL assíncrono para Python
- `sqlalchemy[asyncio]`: ORM com suporte assíncrono

## Notas

- O PostgreSQL usa Alpine Linux (imagem pequena e leve)
- Dados são persistidos em um volume Docker (`postgres_data`)
- Health check verifica se o PostgreSQL está pronto a cada 10 segundos
