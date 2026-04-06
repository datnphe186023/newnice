"""
Seed script to populate initial data for Newnice website
Run with: python -m app.seed
"""
import asyncio
from slugify import slugify

from app.core.database import async_session_maker, init_db
from app.core.security import get_password_hash
from app.models import Category, Brand, Product, AdminUser


async def seed_categories():
    """Seed product categories"""
    categories = [
        {
            "name": "Phim cách nhiệt ô tô",
            "description": "Phim cách nhiệt cao cấp dành cho ô tô, giảm nhiệt và chống UV hiệu quả",
            "sort_order": 1
        },
        {
            "name": "Phim đổi màu xe",
            "description": "Phim đổi màu xe cao cấp - thay đổi diện mạo xe theo phong cách riêng",
            "sort_order": 2
        },
        {
            "name": "Phim cách nhiệt nhà kính",
            "description": "Phim dán kính nhà, văn phòng - cách nhiệt, chống nắng hiệu quả",
            "sort_order": 3
        },
    ]
    
    async with async_session_maker() as session:
        for cat_data in categories:
            category = Category(
                name=cat_data["name"],
                slug=slugify(cat_data["name"]),
                description=cat_data["description"],
                sort_order=cat_data["sort_order"],
                is_active=True
            )
            session.add(category)
        await session.commit()
        print(f"✓ Seeded {len(categories)} categories")


async def seed_brands():
    """Seed product brands"""
    brands = [
        {"name": "3M", "country": "Mỹ", "description": "Thương hiệu phim cách nhiệt hàng đầu thế giới"},
        {"name": "LLumar", "country": "Mỹ", "description": "Phim cách nhiệt cao cấp từ Eastman"},
        {"name": "V-KOOL", "country": "Mỹ", "description": "Phim cách nhiệt công nghệ nano ceramic"},
        {"name": "SunTek", "country": "Mỹ", "description": "Phim cách nhiệt chất lượng cao"},
        {"name": "Ntech", "country": "Hàn Quốc", "description": "Phim cách nhiệt Hàn Quốc"},
    ]
    
    async with async_session_maker() as session:
        for brand_data in brands:
            brand = Brand(
                name=brand_data["name"],
                slug=slugify(brand_data["name"]),
                country=brand_data["country"],
                description=brand_data["description"],
                is_active=True
            )
            session.add(brand)
        await session.commit()
        print(f"✓ Seeded {len(brands)} brands")


async def seed_products():
    """Seed sample products"""
    products = [
        {
            "name": "3M Crystalline CR90",
            "short_description": "Phim cách nhiệt cao cấp nhất của 3M với độ trong suốt vượt trội",
            "description": """
            <h3>3M Crystalline CR90 - Phim cách nhiệt hàng đầu</h3>
            <p>3M Crystalline là dòng phim cách nhiệt cao cấp nhất của 3M, sử dụng công nghệ nano đa lớp độc quyền.</p>
            <h4>Ưu điểm nổi bật:</h4>
            <ul>
                <li>Độ trong suốt cao nhất trong các dòng phim cách nhiệt</li>
                <li>Không gây nhiễu sóng điện thoại, GPS</li>
                <li>Chặn 99.9% tia UV có hại</li>
                <li>Giảm nhiệt hồng ngoại lên đến 97%</li>
            </ul>
            """,
            "film_type": "ceramic",
            "vlt": 90,
            "uv_rejection": 99,
            "ir_rejection": 97,
            "heat_rejection": 60,
            "warranty_years": 10,
            "is_featured": True,
            "category_slug": "phim-cach-nhiet-o-to",
            "brand_slug": "3m"
        },
        {
            "name": "3M Crystalline CR70",
            "short_description": "Cân bằng hoàn hảo giữa độ trong và hiệu quả cách nhiệt",
            "film_type": "ceramic",
            "vlt": 70,
            "uv_rejection": 99,
            "ir_rejection": 97,
            "heat_rejection": 62,
            "warranty_years": 10,
            "is_featured": True,
            "category_slug": "phim-cach-nhiet-o-to",
            "brand_slug": "3m"
        },
        {
            "name": "LLumar ATR 20",
            "short_description": "Phim cách nhiệt LLumar cho vẻ ngoài sang trọng",
            "film_type": "ceramic",
            "vlt": 20,
            "uv_rejection": 99,
            "ir_rejection": 95,
            "heat_rejection": 65,
            "warranty_years": 7,
            "is_featured": True,
            "category_slug": "phim-cach-nhiet-o-to",
            "brand_slug": "llumar"
        },
        {
            "name": "V-KOOL VK70",
            "short_description": "Phim cách nhiệt V-KOOL độ trong cao",
            "film_type": "ceramic",
            "vlt": 70,
            "uv_rejection": 99,
            "ir_rejection": 94,
            "heat_rejection": 55,
            "warranty_years": 7,
            "is_featured": False,
            "category_slug": "phim-cach-nhiet-o-to",
            "brand_slug": "v-kool"
        },
    ]
    
    async with async_session_maker() as session:
        from sqlalchemy import select
        
        for prod_data in products:
            # Get category
            cat_result = await session.execute(
                select(Category).where(Category.slug == prod_data.pop("category_slug"))
            )
            category = cat_result.scalar_one_or_none()
            
            # Get brand
            brand_result = await session.execute(
                select(Brand).where(Brand.slug == prod_data.pop("brand_slug"))
            )
            brand = brand_result.scalar_one_or_none()
            
            product = Product(
                **prod_data,
                slug=slugify(prod_data["name"]),
                category_id=category.id if category else None,
                brand_id=brand.id if brand else None,
                is_contact_price=True,
                is_active=True
            )
            session.add(product)
        
        await session.commit()
        print(f"✓ Seeded {len(products)} products")


async def seed_admin():
    """Seed admin user"""
    async with async_session_maker() as session:
        admin = AdminUser(
            email="admin@newnice.vn",
            password_hash=get_password_hash("admin123"),
            full_name="Administrator",
            role="super_admin",
            is_active=True
        )
        session.add(admin)
        await session.commit()
        print("✓ Seeded admin user (admin@newnice.vn / admin123)")


async def main():
    print("🌱 Seeding database...")
    await init_db()
    await seed_categories()
    await seed_brands()
    await seed_products()
    await seed_admin()
    print("✅ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(main())
