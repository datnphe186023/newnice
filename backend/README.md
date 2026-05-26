# AutoFilm Backend

FastAPI backend for the AutoFilm automotive window film website.

## Setup

```bash
# Development (recommended using a venv)
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt  # if present, otherwise use poetry

# If you use Poetry:
pip install poetry
poetry install

# Create environment file
cp .env.example .env

# Local dev run (reloads on code changes)
export DATABASE_URL="postgresql+asyncpg://autofilm:autofilm@localhost:5432/autofilm"
export DEBUG=True
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run migrations (Alembic)
alembic upgrade head

# Seed the database (creates first admin and required lookup rows)
python -m app.seed

# Running inside Docker (dev compose uses postgres:16.10-alpine3.22)
# Example: run migrations in the backend container
docker compose -f docker-compose.dev.yml run --rm backend \
	sh -c "alembic upgrade head"

# Seed in container:
docker compose -f docker-compose.dev.yml run --rm backend \
	sh -c "python -m app.seed"
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── api/           # API routes
├── core/          # Config, database, security
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── services/      # Business logic
└── utils/         # Utilities
```
