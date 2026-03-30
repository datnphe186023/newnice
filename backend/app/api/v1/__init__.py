from fastapi import APIRouter

from app.api.v1.endpoints import products, categories, brands, quotes, auth, posts

api_router = APIRouter(prefix="/api/v1")

# Public routes
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(brands.router)
api_router.include_router(quotes.router)
api_router.include_router(posts.router)
api_router.include_router(auth.router)
