"""
Seed script to populate initial data for Newnice website.
Run with: python -m app.seed
"""
import asyncio
from slugify import slugify
from sqlalchemy import select

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
        seeded = 0
        for d in categories:
            slug = slugify(d["name"])
            category = (await session.execute(
                select(Category).where(Category.slug == slug)
            )).scalar_one_or_none()

            if category:
                category.name = d["name"]
                category.description = d["description"]
                category.sort_order = d["sort_order"]
                category.is_active = True
            else:
                session.add(Category(
                    name=d["name"], slug=slug,
                    description=d["description"], sort_order=d["sort_order"], is_active=True,
                ))
                seeded += 1

        await session.commit()
        print(f"✓ Seeded {seeded} categories ({len(categories) - seeded} existing)")


async def seed_brands():
    brands = [
        {"name": "Newnice", "country": "Việt Nam", "description": "Thương hiệu phim cách nhiệt & PPF Việt Nam — chất lượng cao, giá tốt nhất"},
    ]
    async with async_session_maker() as session:
        seeded = 0
        for d in brands:
            slug = slugify(d["name"])
            brand = (await session.execute(
                select(Brand).where(Brand.slug == slug)
            )).scalar_one_or_none()

            if brand:
                brand.name = d["name"]
                brand.country = d["country"]
                brand.description = d["description"]
                brand.is_active = True
            else:
                session.add(Brand(
                    name=d["name"], slug=slug,
                    country=d["country"], description=d["description"], is_active=True,
                ))
                seeded += 1

        await session.commit()
        print(f"✓ Seeded {seeded} brands ({len(brands) - seeded} existing)")


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
        seeded = 0
        for d in products:
            product_data = d.copy()
            cat = (await session.execute(
                select(Category).where(Category.slug == product_data.pop("category_slug"))
            )).scalar_one_or_none()
            brand = (await session.execute(
                select(Brand).where(Brand.slug == product_data.pop("brand_slug"))
            )).scalar_one_or_none()

            is_contact = product_data.pop("is_contact_price", False)
            slug = slugify(product_data["name"])
            product = (await session.execute(
                select(Product).where(Product.slug == slug)
            )).scalar_one_or_none()

            values = {
                **product_data,
                "category_id": cat.id if cat else None,
                "brand_id": brand.id if brand else None,
                "is_contact_price": is_contact,
                "is_active": True,
            }

            if product:
                for field, value in values.items():
                    setattr(product, field, value)
            else:
                session.add(Product(**values, slug=slug))
                seeded += 1

        await session.commit()
        print(f"✓ Seeded {seeded} products ({len(products) - seeded} existing)")


async def seed_admin():
    async with async_session_maker() as session:
        email = "admin@newnice.vn"
        admin = (await session.execute(
            select(AdminUser).where(AdminUser.email == email)
        )).scalar_one_or_none()

        if admin:
            admin.full_name = admin.full_name or "Administrator"
            admin.role = admin.role or "super_admin"
            admin.is_active = True
            message = "✓ Admin user already exists (admin@newnice.vn)"
        else:
            session.add(AdminUser(
                email=email,
                password_hash=get_password_hash("admin123"),
                full_name="Administrator",
                role="super_admin",
                is_active=True,
            ))
            message = "✓ Seeded admin user (admin@newnice.vn / admin123)"

        await session.commit()
        print(message)


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
