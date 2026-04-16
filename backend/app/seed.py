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
            "name": "Phim cách nhiệt Newnice",
            "description": "Các dòng phim cách nhiệt thương hiệu Newnice — Eco, Premium, Crystal, Royal",
            "sort_order": 1,
        },
        {
            "name": "PPF Newnice",
            "description": "Phim bảo vệ sơn PPF thương hiệu Newnice — bảo vệ toàn diện, chống trầy xước",
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
        {"name": "Newnice", "country": "Việt Nam", "description": "Thương hiệu phim cách nhiệt & PPF Việt Nam — chất lượng cao, giá tốt nhất"},
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
    products = [
        # ── Phim cách nhiệt Newnice ────────────────────────────────────────
        {
            "name": "Newnice Eco",
            "film_code": "NE",
            "short_description": "Gói phim cách nhiệt Newnice Eco — tiết kiệm, hiệu quả cơ bản",
            "price_sedan": 5_800_000, "price_suv": 7_000_000,
            "vlt": 75, "uv_rejection": 99, "ir_rejection": 80, "heat_rejection": 45,
            "warranty_years": 5, "is_featured": True,
            "category_slug": "phim-cach-nhiet-newnice", "brand_slug": "newnice",
        },
        {
            "name": "Newnice Premium",
            "film_code": "NP",
            "short_description": "Gói phim cách nhiệt Newnice Premium — cân bằng hoàn hảo giữa giá và chất lượng",
            "price_sedan": 10_500_000, "price_suv": 11_500_000,
            "vlt": 70, "uv_rejection": 99, "ir_rejection": 90, "heat_rejection": 55,
            "warranty_years": 7, "is_featured": True,
            "category_slug": "phim-cach-nhiet-newnice", "brand_slug": "newnice",
        },
        {
            "name": "Newnice Crystal",
            "film_code": "NC",
            "short_description": "Gói phim cách nhiệt Newnice Crystal — độ trong cao, cách nhiệt vượt trội",
            "price_sedan": 12_500_000, "price_suv": 14_500_000,
            "vlt": 65, "uv_rejection": 99, "ir_rejection": 95, "heat_rejection": 62,
            "warranty_years": 7, "is_featured": True,
            "category_slug": "phim-cach-nhiet-newnice", "brand_slug": "newnice",
        },
        {
            "name": "Newnice Royal",
            "film_code": "NR",
            "short_description": "Gói phim cách nhiệt Newnice Royal — dòng cao cấp nhất, cách nhiệt tối đa",
            "price_sedan": 15_500_000, "price_suv": 17_500_000,
            "vlt": 60, "uv_rejection": 99, "ir_rejection": 97, "heat_rejection": 68,
            "warranty_years": 10, "is_featured": True,
            "category_slug": "phim-cach-nhiet-newnice", "brand_slug": "newnice",
        },
        # ── PPF Newnice ────────────────────────────────────────────────────
        {
            "name": "Newnice PPF Standard",
            "film_code": "PPF-STD",
            "short_description": "Phim PPF Newnice Standard — bảo vệ sơn xe khỏi trầy xước, đá bắn",
            "price_sedan": None, "price_suv": None, "is_contact_price": True,
            "warranty_years": 5, "is_featured": True,
            "category_slug": "ppf-newnice", "brand_slug": "newnice",
        },
        {
            "name": "Newnice PPF Premium",
            "film_code": "PPF-PRE",
            "short_description": "Phim PPF Newnice Premium — tự phục hồi vết xước nhỏ, bảo vệ toàn diện",
            "price_sedan": None, "price_suv": None, "is_contact_price": True,
            "warranty_years": 7, "is_featured": True,
            "category_slug": "ppf-newnice", "brand_slug": "newnice",
        },
        {
            "name": "Newnice PPF Crystal",
            "film_code": "PPF-CRY",
            "short_description": "Phim PPF Newnice Crystal — trong suốt tuyệt đối, giữ màu sơn gốc hoàn hảo",
            "price_sedan": None, "price_suv": None, "is_contact_price": True,
            "warranty_years": 10, "is_featured": False,
            "category_slug": "ppf-newnice", "brand_slug": "newnice",
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
