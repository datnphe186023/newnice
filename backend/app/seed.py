"""
Reset and seed baseline data for the Newnice website.

Run with:
    python -m app.seed

This script resets seed-owned catalog/admin data only:
- admin_users
- product_images
- products
- categories
- brands

It intentionally does not delete quotes, contacts, warranty records, dealers,
film packages, posts, or site settings.
"""
import asyncio

from slugify import slugify
from sqlalchemy import delete, select

from app.core.database import async_session_maker, init_db
from app.core.security import get_password_hash
from app.models import AdminUser, Brand, Category, Product, ProductImage


ADMIN_EMAIL = "admin@newnice.vn"
ADMIN_PASSWORD = "007584"


CATEGORIES = [
    {
        "name": "Phim cách nhiệt Newnice",
        "slug": "phim-cach-nhiet-newnice",
        "description": "Các dòng phim cách nhiệt ô tô Newnice - Eco, Plus, Pro, Royal.",
        "sort_order": 1,
    },
    {
        "name": "PPF Newnice",
        "slug": "ppf-newnice",
        "description": "Phim bảo vệ sơn PPF Newnice - bảo vệ toàn diện, chống trầy xước.",
        "sort_order": 2,
    },
    {
        "name": "Film cách nhiệt nhà kính",
        "slug": "film-cach-nhiet-nha-kinh",
        "description": "Film cách nhiệt dành cho nhà kính, văn phòng và công trình dân dụng.",
        "sort_order": 3,
    },
]


BRANDS = [
    {
        "name": "Newnice",
        "slug": "newnice",
        "country": "Việt Nam",
        "description": "Thương hiệu phim cách nhiệt & PPF Việt Nam - chất lượng cao, giá tốt.",
    },
]


PRODUCTS = [
    {
        "name": "Newnice Eco",
        "film_code": "NE",
        "short_description": "Gói phim cách nhiệt Newnice Eco - tiết kiệm, hiệu quả cơ bản.",
        "price_sedan": "Sedan: 5.500.000 đ",
        "price_suv": "SUV: 6.700.000 đ",
        "vlt": 75,
        "uv_rejection": 99,
        "ir_rejection": 80,
        "heat_rejection": 45,
        "warranty_years": 5,
        "is_featured": True,
        "sort_order": 1,
        "category_slug": "phim-cach-nhiet-newnice",
        "brand_slug": "newnice",
    },
    {
        "name": "Newnice Plus",
        "film_code": "PLUS",
        "short_description": "Gói phim cách nhiệt Newnice Plus - cân bằng giữa hiệu quả cách nhiệt và chi phí.",
        "price_sedan": "Sedan: 7.500.000 đ",
        "price_suv": "SUV: 8.700.000 đ",
        "vlt": 70,
        "uv_rejection": 99,
        "ir_rejection": 90,
        "heat_rejection": 55,
        "warranty_years": 7,
        "is_featured": True,
        "sort_order": 2,
        "category_slug": "phim-cach-nhiet-newnice",
        "brand_slug": "newnice",
    },
    {
        "name": "Newnice Pro",
        "film_code": "PRO",
        "short_description": "Gói phim cách nhiệt Newnice Pro - hiệu quả cách nhiệt cao cho nhu cầu sử dụng chuyên sâu.",
        "price_sedan": "Sedan: 11.500.000 đ",
        "price_suv": "SUV: 12.900.000 đ",
        "vlt": 65,
        "uv_rejection": 99,
        "ir_rejection": 95,
        "heat_rejection": 62,
        "warranty_years": 7,
        "is_featured": True,
        "sort_order": 3,
        "category_slug": "phim-cach-nhiet-newnice",
        "brand_slug": "newnice",
    },
    {
        "name": "Newnice Royal",
        "film_code": "NR",
        "short_description": "Gói phim cách nhiệt Newnice Royal - cao cấp nhất, cách nhiệt tối đa.",
        "price_sedan": "Sedan: 14.000.000 đ",
        "price_suv": "SUV: 15.500.000 đ",
        "vlt": 60,
        "uv_rejection": 99,
        "ir_rejection": 97,
        "heat_rejection": 68,
        "warranty_years": 10,
        "is_featured": True,
        "sort_order": 4,
        "category_slug": "phim-cach-nhiet-newnice",
        "brand_slug": "newnice",
    },
    {
        "name": "Newnice PPF Standard",
        "film_code": "PPF-STD",
        "short_description": "Phim PPF Newnice Standard - bảo vệ sơn xe khỏi trầy xước, đá bắn.",
        "price_sedan": None,
        "price_suv": None,
        "is_contact_price": True,
        "warranty_years": 5,
        "is_featured": True,
        "sort_order": 5,
        "category_slug": "ppf-newnice",
        "brand_slug": "newnice",
    },
    {
        "name": "Newnice PPF Premium",
        "film_code": "PPF-PRE",
        "short_description": "Phim PPF Newnice Premium - tự phục hồi vết xước nhỏ, bảo vệ toàn diện.",
        "price_sedan": None,
        "price_suv": None,
        "is_contact_price": True,
        "warranty_years": 7,
        "is_featured": True,
        "sort_order": 6,
        "category_slug": "ppf-newnice",
        "brand_slug": "newnice",
    },
    {
        "name": "Newnice PPF Crystal",
        "film_code": "PPF-CRY",
        "short_description": "Phim PPF Newnice Crystal - trong suốt, giữ màu sơn gốc hoàn hảo.",
        "price_sedan": None,
        "price_suv": None,
        "is_contact_price": True,
        "warranty_years": 10,
        "is_featured": False,
        "sort_order": 7,
        "category_slug": "ppf-newnice",
        "brand_slug": "newnice",
    },
]


async def reset_seed_data():
    async with async_session_maker() as session:
        await session.execute(delete(ProductImage))
        await session.execute(delete(Product))
        await session.execute(delete(Category))
        await session.execute(delete(Brand))
        await session.execute(delete(AdminUser))
        await session.commit()
        print("✓ Cleared seed-owned admin and catalog data")


async def seed_categories():
    async with async_session_maker() as session:
        for data in CATEGORIES:
            session.add(
                Category(
                    name=data["name"],
                    slug=data["slug"],
                    description=data["description"],
                    sort_order=data["sort_order"],
                    is_active=True,
                )
            )

        await session.commit()
        print(f"✓ Seeded {len(CATEGORIES)} categories")


async def seed_brands():
    async with async_session_maker() as session:
        for data in BRANDS:
            session.add(
                Brand(
                    name=data["name"],
                    slug=data["slug"],
                    country=data["country"],
                    description=data["description"],
                    is_active=True,
                )
            )

        await session.commit()
        print(f"✓ Seeded {len(BRANDS)} brands")


async def seed_products():
    async with async_session_maker() as session:
        categories = {
            row.slug: row
            for row in (await session.execute(select(Category))).scalars().all()
        }
        brands = {
            row.slug: row
            for row in (await session.execute(select(Brand))).scalars().all()
        }

        for data in PRODUCTS:
            product_data = data.copy()
            category_slug = product_data.pop("category_slug")
            brand_slug = product_data.pop("brand_slug")
            category = categories.get(category_slug)
            brand = brands.get(brand_slug)

            if not category:
                raise RuntimeError(f"Missing category for product seed: {category_slug}")
            if not brand:
                raise RuntimeError(f"Missing brand for product seed: {brand_slug}")

            is_contact_price = product_data.pop("is_contact_price", False)
            session.add(
                Product(
                    **product_data,
                    slug=slugify(product_data["name"]),
                    category_id=category.id,
                    brand_id=brand.id,
                    is_contact_price=is_contact_price,
                    is_active=True,
                )
            )

        await session.commit()
        print(f"✓ Seeded {len(PRODUCTS)} products")


async def seed_admin():
    async with async_session_maker() as session:
        session.add(
            AdminUser(
                email=ADMIN_EMAIL,
                password_hash=get_password_hash(ADMIN_PASSWORD),
                full_name="Administrator",
                role="super_admin",
                is_active=True,
            )
        )
        await session.commit()
        print(f"✓ Seeded admin user ({ADMIN_EMAIL} / {ADMIN_PASSWORD})")


async def main():
    print("🌱 Resetting and seeding database...")
    await init_db()
    await reset_seed_data()
    await seed_categories()
    await seed_brands()
    await seed_products()
    await seed_admin()
    print("✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
