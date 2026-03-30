# AutoFilm Backend

FastAPI backend for the AutoFilm automotive window film website.

## Setup

```bash
# Install dependencies
pip install -e .

# Create .env file
cp .env.example .env

# Run the server
uvicorn app.main:app --reload

# Seed the database
python -m app.seed
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
