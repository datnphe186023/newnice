from fastapi import APIRouter

from app.api.v1.endpoints import (
	products,
	categories,
	brands,
	quotes,
	auth,
	posts,
	upload,
	admin_posts,
	admin_settings,
	sitemap,
)

api_router = APIRouter(prefix="/api/v1")

# Public routes
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(brands.router)
api_router.include_router(quotes.router)
api_router.include_router(posts.router)
api_router.include_router(auth.router)
api_router.include_router(sitemap.router)

# Admin routes (require authentication)
api_router.include_router(upload.router, prefix="/admin", tags=["Admin - Upload"])
api_router.include_router(admin_posts.router, prefix="/admin")
api_router.include_router(admin_settings.router, prefix="/admin")
