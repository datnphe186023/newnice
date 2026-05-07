# AutoFilm Backend

FastAPI backend for the AutoFilm automotive window film website.

## Setup

```bash
# Install dependencies
pip install poetry
poetry install

# Create .env file
cp .env.example .env

# Run migrations
poetry run alembic upgrade head

# Run the server
poetry run uvicorn app.main:app --reload

# Seed the database
poetry run python -m app.seed
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
