# API Routes Validation

## Backend API Status

### Public Endpoints

#### Products
- [x] GET /api/v1/products - List products with filters
- [x] GET /api/v1/products/{slug} - Get product by slug
- [x] GET /api/v1/products/admin/{id} - Get product by ID (admin)

#### Categories
- [x] GET /api/v1/categories - List categories
- [x] GET /api/v1/categories/{slug} - Get category by slug

#### Brands
- [x] GET /api/v1/brands - List active brands
- [x] GET /api/v1/brands/admin/all - List all brands (admin)

#### Posts
- [x] GET /api/v1/posts - List posts
- [x] GET /api/v1/posts/{slug} - Get post by slug

#### Quotes & Contacts
- [x] GET /api/v1/quotes - List quotes (admin)
- [x] GET /api/v1/contacts - List contacts (admin)
- [x] POST /api/v1/quotes - Create quote request
- [x] POST /api/v1/contact - Submit contact form
- [x] PUT /api/v1/quotes/{id} - Update quote status (admin)
- [x] PUT /api/v1/contacts/{id}/read - Mark contact as read (admin)

#### Authentication
- [x] POST /api/v1/auth/login - Admin login
- [x] POST /api/v1/auth/register - Admin registration
- [x] GET /api/v1/auth/me - Get current user

#### Sitemap
- [x] GET /api/v1/sitemap.xml - XML sitemap for SEO

### Admin Endpoints (Protected)

#### Products
- [x] POST /api/v1/products - Create product
- [x] PUT /api/v1/products/{id} - Update product
- [x] DELETE /api/v1/products/{id} - Delete product
- [x] POST /api/v1/admin/upload - Upload image

#### Categories
- [x] POST /api/v1/categories - Create category
- [x] PUT /api/v1/categories/{id} - Update category
- [x] DELETE /api/v1/categories/{id} - Delete category
- [x] PUT /api/v1/categories/admin/reorder - Reorder categories

#### Brands
- [x] GET /api/v1/brands/admin/all - List all brands (including inactive)
- [x] POST /api/v1/brands - Create brand
- [x] PUT /api/v1/brands/{id} - Update brand
- [x] DELETE /api/v1/brands/{id} - Delete brand

#### Posts
- [x] POST /api/v1/admin/posts - Create post
- [x] PATCH /api/v1/admin/posts/{id} - Update post
- [x] DELETE /api/v1/admin/posts/{id} - Delete post

#### Settings
- [x] GET /api/v1/admin/settings - Get site settings
- [x] PATCH /api/v1/admin/settings - Update site settings

#### File Upload
- [x] POST /api/v1/admin/upload - Upload single file
- [x] POST /api/v1/admin/upload/multiple - Upload multiple files
- [x] DELETE /api/v1/admin/upload - Delete file

### Health Check
- [x] GET /api/v1/health - Health check endpoint

## Frontend Routes Status

### Public Pages
- [x] / - Home page
- [x] /san-pham - Product listing
- [x] /san-pham/[slug] - Product detail
- [x] /danh-muc/[slug] - Category page
- [x] /tin-tuc - News/posts listing
- [x] /tin-tuc/[slug] - News/post detail
- [x] /lien-he - Contact form page
- [x] /bao-gia - Quote request form page

### Admin Pages
- [x] /admin - Admin dashboard
- [x] /admin/login - Admin login
- [x] /admin/products - Product management
- [x] /admin/products/new - Create new product
- [x] /admin/products/[id] - Edit product
- [x] /admin/categories - Category management
- [x] /admin/brands - Brand management
- [x] /admin/posts - Post management
- [x] /admin/quotes - Quote management
- [x] /admin/contacts - Contact management
- [x] /admin/settings - Site settings

## Integration Checklist

Before Production Deployment:

- [ ] All API endpoints tested with proper authentication
- [ ] CORS properly configured for frontend domain
- [ ] Admin endpoints return 401 for unauthenticated requests
- [ ] Rate limiting configured (if needed)
- [ ] Request/response validation working
- [ ] Error messages are informative but don't expose sensitive data
- [ ] File upload has proper validation and size limits
- [ ] Database queries are optimized (no N+1 queries)
- [ ] Timestamps are in UTC
- [ ] Soft deletes used where appropriate

## Testing the API

### Local Development
```bash
# Start backend
cd backend
poetry install
uvicorn app.main:app --reload

# Test endpoints
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/products
```

### Production Health Check
```bash
curl https://yourdomain.com/api/v1/health
```

### Admin Authentication Flow
1. POST /api/v1/auth/login with credentials
2. Receive JWT token
3. Use token in Authorization: Bearer <token> header for admin endpoints
4. Token expires after configured time (default: 24 hours)
5. GET /api/v1/auth/me to verify current user
