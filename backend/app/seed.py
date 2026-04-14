"""
Seed script to populate initial data for Newnice website.
Run with: python -m app.seed
"""
import asyncio
from slugify import slugify

from app.core.database import async_session_maker, init_db
from app.core.security import get_password_hash
from app.models import Category, Brand, Product, AdminUser


async def seed_categories():
    categories = [
        {
            "name": "Phim cách nhiệt 3M",
            "description": "Các dòng phim cách nhiệt chính hãng 3M — Crystalline, CR BLK, Ceramic IR",
            "sort_order": 1,
        },
        {
            "name": "Phim cách nhiệt Newnice",
            "description": "Các dòng phim cách nhiệt thương hiệu Newnice — chất lượng cao, giá tốt",
            "sort_order": 2,
        },
    ]
    async with async_session_maker() as session:
        for d in categories:
            session.add(Category(
                name=d["name"], slug=slugify(d["name"]),
                description=d["description"], sort_order=d["sort_order"], is_active=True,
            ))
        await session.commit()
        print(f"✓ Seeded {len(categories)} categories")


async def seed_brands():
    brands = [
        {"name": "3M",      "country": "Mỹ",       "description": "Thương hiệu phim cách nhiệt hàng đầu thế giới"},
        {"name": "Newnice", "country": "Việt Nam",  "description": "Thương hiệu phim cách nhiệt Việt Nam — chất lượng cao, giá tốt nhất"},
    ]
    async with async_session_maker() as session:
        for d in brands:
            session.add(Brand(
                name=d["name"], slug=slugify(d["name"]),
                country=d["country"], description=d["description"], is_active=True,
            ))
        await session.commit()
        print(f"✓ Seeded {len(brands)} brands")


async def seed_products():
    """
    Seed film products based on the 3M price table.
    Each product = one film package (brand + film code).
    Prices are SEDAN / SUV totals from the price table.
    """
    products = [
        # ── 3M Crystalline CR BLK PRO ──────────────────────────────────────
        {
            "name": "3M Crystalline CR BLK PRO",
            "film_code": "CR BLK PRO",
            "short_description": "Gói phim cách nhiệt 3M Crystalline CR BLK PRO — dòng cao cấp nhất, kính trước CR BLK 40",
            "price_sedan": 15_500_000,
            "price_suv":   18_300_000,
            "vlt": 40, "uv_rejection": 99, "ir_rejection": 97, "heat_rejection": 65,
            "warranty_years": 10, "is_featured": True,
            "category_slug": "phim-cach-nhiet-3m", "brand_slug": "3m",
        },
        # ── 3M Crystalline CR BLK ──────────────────────────────────────────
        {
            "name": "3M Crystalline CR BLK",
            "film_code": "CR BLK",
            "short_description": "Gói phim cách nhiệt 3M Crystalline CR BLK — kính trước CR 50, kính sườn CR BLK 15/35",
            "price_sedan": 14_700_000,
            "price_suv":   17_500_000,
            "vlt": 50, "uv_rejection": 99, "ir_rejection": 97, "heat_rejection": 62,
            "warranty_years": 10, "is_featured": True,
            "category_slug": "phim-cach-nhiet-3m", "brand_slug": "3m",
        },
        # ── 3M Best Seller 01 ──────────────────────────────────────────────
        {
            "name": "3M Best Seller 01",
            "film_code": "BS01",
            "short_description": "Gói phim 3M Best Seller 01 — kính trước CR BLK 40, kính sườn CR BLK 15/35",
            "price_sedan": 12_800_000,
            "price_suv":   14_300_000,
            "vlt": 40, "uv_rejection": 99, "ir_rejection": 95, "heat_rejection": 60,
            "warranty_years": 10, "is_featured": True,
            "category_slug": "phim-cach-nhiet-3m", "brand_slug": "3m",
        },
        # ── 3M Best Seller 02 ──────────────────────────────────────────────
        {
            "name": "3M Best Seller 02",
            "film_code": "BS02",
            "short_description": "Gói phim 3M Best Seller 02 — kính trước CR BLK 50, kính sườn IR 15/25",
            "price_sedan": 11_200_000,
            "price_suv":   12_700_000,
            "vlt": 50, "uv_rejection": 99, "ir_rejection": 93, "heat_rejection": 58,
            "warranty_years": 10, "is_featured": False,
            "category_slug": "phim-cach-nhiet-3m", "brand_slug": "3m",
        },
        # ── 3M Ceramic IR ──────────────────────────────────────────────────
        {
            "name": "3M Ceramic IR",
            "film_code": "Ceramic IR",
            "short_description": "Gói phim 3M Ceramic IR — kính trước IR 50, kính sườn IR 15/25",
            "price_sedan":  9_000_000,
            "price_suv":   10_500_000,
            "vlt": 50, "uv_rejection": 99, "ir_rejection": 90, "heat_rejection": 55,
            "warranty_years": 10, "is_featured": False,
            "category_slug": "phim-cach-nhiet-3m", "brand_slug": "3m",
        },
        # ── Newnice (template — bạn sẽ cung cấp mã cụ thể sau) ────────────
        {
            "name": "Newnice Premium",
            "film_code": "NNC-PRE",
            "short_description": "Gói phim cách nhiệt Newnice Premium — chất lượng cao, giá tốt nhất thị trường",
            "price_sedan": None,
            "price_suv":   None,
            "is_contact_price": True,
            "vlt": 70, "uv_rejection": 99, "ir_rejection": 95, "heat_rejection": 60,
            "warranty_years": 7, "is_featured": True,
            "category_slug": "phim-cach-nhiet-newnice", "brand_slug": "newnice",
        },
    ]

    async with async_session_maker() as session:
        from sqlalchemy import select

        for d in products:
            cat = (await session.execute(
                select(Category).where(Category.slug == d.pop("category_slug"))
            )).scalar_one_or_none()
            brand = (await session.execute(
                select(Brand).where(Brand.slug == d.pop("brand_slug"))
            )).scalar_one_or_none()

            is_contact = d.pop("is_contact_price", False)
            session.add(Product(
                **d,
                slug=slugify(d["name"]),
                category_id=cat.id if cat else None,
                brand_id=brand.id if brand else None,
                is_contact_price=is_contact,
                is_active=True,
            ))

        await session.commit()
        print(f"✓ Seeded {len(products)} products")


async def seed_admin():
    async with async_session_maker() as session:
        session.add(AdminUser(
            email="admin@newnice.vn",
            password_hash=get_password_hash("admin123"),
            full_name="Administrator",
            role="super_admin",
            is_active=True,
        ))
        await session.commit()
        print("✓ Seeded admin user (admin@newnice.vn / admin123)")


async def main():
    print("🌱 Seeding database...")
    await init_db()
    await seed_categories()
    await seed_brands()
    await seed_products()
    await seed_admin()
    print("✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
