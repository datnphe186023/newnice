# Newnice Website

Automotive Window Film E-commerce Website built with FastAPI + Nuxt.js 3

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Frontend**: Nuxt.js 3, Vue.js 3, Tailwind CSS
- **Database**: PostgreSQL 16.10 Alpine 3.22 via Docker Compose

## Quick Start

### Option 1: Docker (Recommended)

```bash
docker compose -f docker-compose.dev.yml up -d
```

The development profile starts PostgreSQL automatically, waits for it to be
healthy, then runs Alembic migrations before the API starts.

Production profile:

```bash
# SECRET_KEY, POSTGRES_PASSWORD, SITE_URL, ADMIN_URL, and public Nuxt URLs
# must be set in your shell/environment or .env file
docker compose up -d
```

Docker data is persisted in named volumes:
- `postgres_data` stores PostgreSQL data, including warranty records
- `backend_data` remains available for backend file data

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend

```bash
cd backend
pip install poetry
poetry install
cp .env.example .env

# Initialize database and seed data
poetry run alembic upgrade head
poetry run python -m app.seed

# Run server
poetry run uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
newnice-website/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Config, database, security
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   └── pyproject.toml
│
├── frontend/          # Nuxt.js frontend
│   ├── components/    # Vue components
│   ├── composables/   # Vue composables
│   ├── pages/         # Page routes
│   └── nuxt.config.ts
│
└── docker-compose.yml
```

## Default Admin

After running seed script:
- Email: admin@newnice.vn
- Password: 007584

## API Endpoints

- `GET /api/v1/products` - List products
- `GET /api/v1/products/{slug}` - Product detail
- `GET /api/v1/categories` - List categories
- `GET /api/v1/brands` - List brands
- `POST /api/v1/quotes` - Submit quote request
- `POST /api/v1/contact` - Submit contact form
- `POST /api/v1/auth/login` - Admin login
