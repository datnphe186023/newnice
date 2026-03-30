# AutoFilm Website - Automotive Window Film Platform

## Project Overview

A professional e-commerce website for automotive window films (phim cách nhiệt ô tô), inspired by newaudio.vn design but specialized for the window film industry in Vietnam.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0 with async support
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Image Processing**: Pillow, python-resize-image
- **Validation**: Pydantic v2
- **Task Queue**: Celery + Redis (for email notifications)

### Frontend
- **Framework**: Nuxt.js 3 (Vue.js 3 with SSR)
- **Styling**: Tailwind CSS 3
- **State Management**: Pinia
- **UI Components**: Headless UI, custom components
- **Slider**: Swiper.js
- **Icons**: Heroicons, Font Awesome
- **Forms**: VeeValidate + Yup

### DevOps
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (reverse proxy)
- **CI/CD**: GitHub Actions
- **Hosting**: VPS (Vultr/DigitalOcean) or Vercel (frontend)

## Database Schema

### Core Tables

```sql
-- Categories (Danh mục sản phẩm)
categories:
  - id: UUID
  - name: VARCHAR(255)           -- "Phim cách nhiệt ô tô"
  - slug: VARCHAR(255)           -- "phim-cach-nhiet-o-to"
  - description: TEXT
  - image: VARCHAR(500)
  - banner_image: VARCHAR(500)
  - parent_id: UUID (nullable)
  - sort_order: INTEGER
  - is_active: BOOLEAN
  - meta_title: VARCHAR(255)
  - meta_description: TEXT
  - created_at, updated_at

-- Brands (Thương hiệu)
brands:
  - id: UUID
  - name: VARCHAR(255)           -- "3M", "LLumar", "V-KOOL"
  - slug: VARCHAR(255)
  - logo: VARCHAR(500)
  - description: TEXT
  - country: VARCHAR(100)
  - is_active: BOOLEAN
  - created_at, updated_at

-- Products (Sản phẩm phim)
products:
  - id: UUID
  - name: VARCHAR(255)           -- "3M Crystalline CR90"
  - slug: VARCHAR(255)
  - sku: VARCHAR(50)
  - category_id: UUID (FK)
  - brand_id: UUID (FK)
  - short_description: TEXT
  - description: TEXT (rich HTML)
  - price: DECIMAL(12,0)         -- VND, nullable for "Liên hệ"
  - is_contact_price: BOOLEAN
  - thumbnail: VARCHAR(500)
  - is_featured: BOOLEAN
  - is_active: BOOLEAN
  - sort_order: INTEGER
  - meta_title: VARCHAR(255)
  - meta_description: TEXT
  - created_at, updated_at

-- Product Specifications (Thông số kỹ thuật)
product_specifications:
  - id: UUID
  - product_id: UUID (FK)
  - vlt: INTEGER                 -- Visible Light Transmission (%)
  - uv_rejection: INTEGER        -- UV rejection (%)
  - ir_rejection: INTEGER        -- Infrared rejection (%)
  - heat_rejection: INTEGER      -- Total heat rejection (%)
  - thickness: VARCHAR(50)       -- "2mil", "4mil"
  - warranty_years: INTEGER
  - film_type: ENUM              -- ceramic, carbon, metallic, dyed, hybrid

-- Product Images
product_images:
  - id: UUID
  - product_id: UUID (FK)
  - image_url: VARCHAR(500)
  - thumbnail_url: VARCHAR(500)
  - alt_text: VARCHAR(255)
  - sort_order: INTEGER

-- Car Compatibility (Xe tương thích)
car_brands:
  - id: UUID
  - name: VARCHAR(100)           -- "Toyota", "Mercedes"
  - logo: VARCHAR(500)
  
car_models:
  - id: UUID
  - brand_id: UUID (FK)
  - name: VARCHAR(100)           -- "Camry", "C-Class"
  - year_from: INTEGER
  - year_to: INTEGER

product_car_compatibility:
  - product_id: UUID (FK)
  - car_model_id: UUID (FK)

-- Quote Requests (Yêu cầu báo giá)
quote_requests:
  - id: UUID
  - customer_name: VARCHAR(255)
  - phone: VARCHAR(20)
  - email: VARCHAR(255)
  - car_brand: VARCHAR(100)
  - car_model: VARCHAR(100)
  - car_year: INTEGER
  - product_id: UUID (FK, nullable)
  - film_type_preference: VARCHAR(100)
  - message: TEXT
  - status: ENUM                 -- pending, contacted, quoted, completed
  - admin_notes: TEXT
  - created_at, updated_at

-- Contact Messages
contacts:
  - id: UUID
  - name: VARCHAR(255)
  - phone: VARCHAR(20)
  - email: VARCHAR(255)
  - subject: VARCHAR(255)
  - message: TEXT
  - is_read: BOOLEAN
  - created_at

-- Blog/News
posts:
  - id: UUID
  - title: VARCHAR(255)
  - slug: VARCHAR(255)
  - excerpt: TEXT
  - content: TEXT
  - thumbnail: VARCHAR(500)
  - author_id: UUID (FK)
  - is_published: BOOLEAN
  - published_at: TIMESTAMP
  - meta_title: VARCHAR(255)
  - meta_description: TEXT
  - created_at, updated_at

-- Admin Users
admin_users:
  - id: UUID
  - email: VARCHAR(255)
  - password_hash: VARCHAR(255)
  - full_name: VARCHAR(255)
  - role: ENUM                   -- super_admin, admin, editor
  - is_active: BOOLEAN
  - last_login: TIMESTAMP
  - created_at, updated_at

-- Site Settings
site_settings:
  - key: VARCHAR(100)
  - value: TEXT
  - type: ENUM                   -- text, html, image, json
```

## API Endpoints

### Public API

```
GET    /api/v1/categories
GET    /api/v1/categories/{slug}
GET    /api/v1/products
GET    /api/v1/products/{slug}
GET    /api/v1/products/featured
GET    /api/v1/brands
GET    /api/v1/brands/{slug}
GET    /api/v1/posts
GET    /api/v1/posts/{slug}
POST   /api/v1/quotes
POST   /api/v1/contact
GET    /api/v1/car-brands
GET    /api/v1/car-models?brand_id=
GET    /api/v1/settings/{key}
GET    /api/v1/search?q=
```

### Admin API

```
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout

# Products
GET    /api/v1/admin/products
POST   /api/v1/admin/products
GET    /api/v1/admin/products/{id}
PUT    /api/v1/admin/products/{id}
DELETE /api/v1/admin/products/{id}
POST   /api/v1/admin/products/{id}/images

# Categories
GET    /api/v1/admin/categories
POST   /api/v1/admin/categories
PUT    /api/v1/admin/categories/{id}
DELETE /api/v1/admin/categories/{id}

# Quotes
GET    /api/v1/admin/quotes
GET    /api/v1/admin/quotes/{id}
PUT    /api/v1/admin/quotes/{id}

# Contacts
GET    /api/v1/admin/contacts
PUT    /api/v1/admin/contacts/{id}/read

# Posts
CRUD   /api/v1/admin/posts

# Settings
GET    /api/v1/admin/settings
PUT    /api/v1/admin/settings

# Upload
POST   /api/v1/admin/upload
```

## Project Structure

```
autofilm-website/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── product.py
│   │   │   ├── category.py
│   │   │   ├── quote.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── product.py
│   │   │   └── ...
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── products.py
│   │   │   │   ├── categories.py
│   │   │   │   ├── quotes.py
│   │   │   │   ├── auth.py
│   │   │   │   └── admin/
│   │   │   │       └── ...
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── product_service.py
│   │   │   ├── image_service.py
│   │   │   └── email_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── security.py
│   ├── alembic/
│   ├── tests/
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── nuxt.config.ts
│   ├── app.vue
│   ├── pages/
│   │   ├── index.vue
│   │   ├── san-pham/
│   │   │   ├── index.vue
│   │   │   └── [slug].vue
│   │   ├── danh-muc/
│   │   │   └── [slug].vue
│   │   ├── bao-gia.vue
│   │   ├── lien-he.vue
│   │   ├── gioi-thieu.vue
│   │   ├── tin-tuc/
│   │   │   ├── index.vue
│   │   │   └── [slug].vue
│   │   └── admin/
│   │       ├── login.vue
│   │       ├── index.vue
│   │       ├── products/
│   │       ├── quotes/
│   │       └── settings/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.vue
│   │   │   ├── Footer.vue
│   │   │   ├── MobileNav.vue
│   │   │   └── FloatingButtons.vue
│   │   ├── home/
│   │   │   ├── HeroSlider.vue
│   │   │   ├── CategoryGrid.vue
│   │   │   └── FeaturedProducts.vue
│   │   ├── product/
│   │   │   ├── ProductCard.vue
│   │   │   ├── ProductGrid.vue
│   │   │   ├── ProductFilters.vue
│   │   │   ├── SpecsTable.vue
│   │   │   └── ImageGallery.vue
│   │   └── forms/
│   │       ├── QuoteForm.vue
│   │       └── ContactForm.vue
│   ├── composables/
│   │   ├── useProducts.ts
│   │   ├── useCategories.ts
│   │   └── useQuote.ts
│   ├── stores/
│   │   ├── auth.ts
│   │   └── cart.ts
│   ├── layouts/
│   │   ├── default.vue
│   │   └── admin.vue
│   ├── assets/
│   │   └── css/
│   │       └── main.css
│   ├── public/
│   │   └── images/
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── nginx/
│   └── nginx.conf
├── .github/
│   └── workflows/
│       └── deploy.yml
├── PROJECT_SPEC.md
├── AGENTS.md
└── .beads/
```

## Product Categories (Vietnamese)

1. **Phim cách nhiệt ô tô** (Automotive Window Film)
   - Phim Ceramic
   - Phim Carbon
   - Phim Metallic
   - Phim Nano

2. **Phim PPF** (Paint Protection Film)
   - PPF trong suốt
   - PPF tự phục hồi

3. **Phim đổi màu xe** (Color Change Wrap)
   - Phim đổi màu mờ
   - Phim đổi màu bóng
   - Phim Chrome

4. **Phim cách nhiệt nhà kính** (Architectural Film)
   - Phim chống nắng
   - Phim an toàn

## Key Features

### Customer-Facing
- [x] Product catalog with filtering (by category, brand, VLT range)
- [x] Product detail with specs comparison
- [x] Quote request form with car model selection
- [x] Search functionality
- [x] Responsive design (mobile-first)
- [x] Fast loading with SSR
- [x] SEO optimized with meta tags
- [x] Zalo/Phone floating buttons

### Admin
- [x] Product CRUD with image upload
- [x] Category management
- [x] Quote request management
- [x] Blog/News management
- [x] Basic analytics dashboard

## SEO Requirements

- Server-side rendering (Nuxt.js)
- Dynamic meta tags per page
- Open Graph tags for social sharing
- XML sitemap generation
- Structured data (JSON-LD) for products
- Canonical URLs
- Vietnamese content optimization

## Performance Targets

- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Time to Interactive: < 3s
- Core Web Vitals: All green
- Lighthouse Score: > 90

## Development Phases

### Phase 1 - MVP (2-3 weeks)
- Basic project setup
- Product catalog (list/detail)
- Category pages
- Quote request form
- Contact page
- Admin: Product & Quote management

### Phase 2 - Enhancement (1-2 weeks)
- Blog/News section
- Advanced filtering
- Image optimization
- SEO improvements

### Phase 3 - Polish (1 week)
- Performance optimization
- Analytics integration
- Final testing
- Deployment

## Getting Started

```bash
# Clone and setup
cd autofilm-website

# Backend
cd backend
poetry install
cp .env.example .env
# Edit .env with your settings
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
cp .env.example .env
npm run dev

# Or use Docker
docker-compose up -d
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/autofilm
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379
UPLOAD_DIR=./uploads
```

### Frontend (.env)
```
NUXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NUXT_PUBLIC_SITE_URL=https://autofilm.vn
```
