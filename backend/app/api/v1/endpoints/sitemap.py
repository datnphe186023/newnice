"""
XML Sitemap endpoint.
Generates a standards-compliant sitemap.xml aggregating:
 - Static pages (home, about, contact, quote, products, blog)
 - All active product pages
 - All published blog posts
 - All active categories
"""
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models import Product, Category
from app.models.content import Post

router = APIRouter(tags=["SEO"])

SITE_URL = settings.SITE_URL.rstrip("/")


def _url(loc: str, lastmod: str | None = None, changefreq: str = "weekly", priority: str = "0.5") -> str:
    lastmod_tag = f"  <lastmod>{lastmod}</lastmod>\n" if lastmod else ""
    return (
        f"<url>\n"
        f"  <loc>{SITE_URL}{loc}</loc>\n"
        f"{lastmod_tag}"
        f"  <changefreq>{changefreq}</changefreq>\n"
        f"  <priority>{priority}</priority>\n"
        f"</url>\n"
    )


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


@router.get("/sitemap.xml", response_class=Response)
async def sitemap(db: Annotated[AsyncSession, Depends(get_db)]):
    """Generate XML sitemap for the website."""
    xml = await _build_sitemap_xml(db)
    return Response(content=xml, media_type="application/xml")


@router.head("/sitemap.xml", response_class=Response)
async def sitemap_head():
    """Allow HEAD checks for sitemap monitors and crawlers."""
    return Response(status_code=200, media_type="application/xml")


async def _build_sitemap_xml(db: AsyncSession) -> str:
    urls: list[str] = []

    # --- Static pages ---
    static_pages = [
        ("/", "daily", "1.0"),
        ("/san-pham", "daily", "0.9"),
        ("/tin-tuc", "weekly", "0.8"),
        ("/lien-he", "monthly", "0.6"),
        ("/bao-gia", "monthly", "0.7"),
    ]
    today = _now()
    for path, freq, pri in static_pages:
        urls.append(_url(path, today, freq, pri))

    # --- Active categories ---
    cats = (await db.execute(
        select(Category).where(Category.is_active == True).order_by(Category.sort_order)
    )).scalars().all()
    for cat in cats:
        urls.append(_url(f"/danh-muc/{cat.slug}", today, "weekly", "0.7"))

    # --- Active products ---
    products = (await db.execute(
        select(Product.slug, Product.updated_at).where(Product.is_active == True)
    )).all()
    for slug, updated_at in products:
        lastmod = updated_at.strftime("%Y-%m-%d") if updated_at else today
        urls.append(_url(f"/san-pham/{slug}", lastmod, "weekly", "0.8"))

    # --- Published blog posts ---
    posts = (await db.execute(
        select(Post.slug, Post.updated_at).where(Post.is_published == True)
        .order_by(Post.published_at.desc())
    )).all()
    for slug, updated_at in posts:
        lastmod = updated_at.strftime("%Y-%m-%d") if updated_at else today
        urls.append(_url(f"/tin-tuc/{slug}", lastmod, "weekly", "0.7"))

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(urls)
        + "</urlset>"
    )
