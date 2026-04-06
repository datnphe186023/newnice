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
    """Seed product brands - Newnice (primary) and 3M only"""
    brands = [
        {"name": "Newnice", "country": "Việt Nam", "description": "Thương hiệu phim cách nhiệt Việt Nam - Chất lượng cao, giá tốt nhất"},
        {"name": "3M", "country": "Mỹ", "description": "Thương hiệu phim cách nhiệt hàng đầu thế giới"},
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
    """Seed sample products - Newnice (featured) and 3M products"""
    products = [
        # Newnice products - FEATURED (primary brand)
        {
            "name": "Newnice Premium IR90",
            "short_description": "Phim cách nhiệt cao cấp Newnice - Độ trong suốt cao, cách nhiệt vượt trội",
            "description": """
            <h3>Newnice Premium IR90 - Phim cách nhiệt cao cấp Việt Nam</h3>
            <p>Newnice Premium IR90 là dòng phim cách nhiệt cao cấp nhất của Newnice, sử dụng công nghệ nano ceramic tiên tiến.</p>
            <h4>Ưu điểm nổi bật:</h4>
            <ul>
                <li>Độ trong suốt cao 90% - Tầm nhìn rõ ràng</li>
                <li>Chặn 99% tia UV có hại</li>
                <li>Giảm nhiệt hồng ngoại lên đến 95%</li>
                <li>Không gây nhiễu sóng điện thoại, GPS</li>
                <li>Bảo hành chính hãng 7 năm</li>
            </ul>
            """,
            "film_type": "ceramic",
            "vlt": 90,
            "uv_rejection": 99,
            "ir_rejection": 95,
            "heat_rejection": 60,
            "warranty_years": 7,
            "is_featured": True,
            "category_slug": "phim-cach-nhiet-o-to",
            "brand_slug": "newnice"
        },
        {
            "name": "Newnice Premium IR70",
            "short_description": "Cân bằng hoàn hảo giữa độ trong và hiệu quả cách nhiệt",
            "description": """
            <h3>Newnice Premium IR70 - Lựa chọn phổ biến nhất</h3>
            <p>Newnice Premium IR70 mang đến sự cân bằng hoàn hảo giữa độ trong suốt và khả năng cách nhiệt.</p>
            <h4>Ưu điểm nổi bật:</h4>
            <ul>
                <li>Độ trong suốt 70% - Phù hợp cho kính sườn</li>
                <li>Chặn 99% tia UV có hại</li>
                <li>Giảm nhiệt hồng ngoại lên đến 96%</li>
                <li>Giá thành hợp lý - Chất lượng cao</li>
            </ul>
            """,
            "film_type": "ceramic",
            "vlt": 70,
            "uv_rejection": 99,
            "ir_rejection": 96,
            "heat_rejection": 62,
            "warranty_years": 7,
            "is_featured": True,
            "category_slug": "phim-cach-nhiet-o-to",
            "brand_slug": "newnice"
        },
        {
            "name": "Newnice Premium IR50",
            "short_description": "Phim cách nhiệt đậm màu - Riêng tư tối đa",
            "description": """
            <h3>Newnice Premium IR50 - Riêng tư và cách nhiệt</h3>
            <p>Newnice Premium IR50 dành cho khách hàng muốn tăng sự riêng tư và cách nhiệt tối đa.</p>
            <h4>Ưu điểm nổi bật:</h4>
            <ul>
                <li>Độ trong suốt 50% - Tăng sự riêng tư</li>
                <li>Chặn 99% tia UV có hại</li>
                <li>Giảm nhiệt hồng ngoại lên đến 97%</li>
                <li>Màu đen sang trọng</li>
            </ul>
            """,
            "film_type": "ceramic",
            "vlt": 50,
            "uv_rejection": 99,
            "ir_rejection": 97,
            "heat_rejection": 68,
            "warranty_years": 7,
            "is_featured": True,
            "category_slug": "phim-cach-nhiet-o-to",
            "brand_slug": "newnice"
        },
        {
            "name": "Newnice Color Change Gloss Black",
            "short_description": "Phim đổi màu đen bóng cao cấp - Sang trọng và bền bỉ",
            "description": """
            <h3>Newnice Color Change Gloss Black</h3>
            <p>Phim đổi màu đen bóng cao cấp, mang đến vẻ ngoài sang trọng cho xe của bạn.</p>
            <h4>Ưu điểm nổi bật:</h4>
            <ul>
                <li>Màu đen bóng sâu - Sang trọng</li>
                <li>Chống trầy xước</li>
                <li>Dễ dàng tháo gỡ khi cần</li>
                <li>Bảo vệ sơn gốc xe</li>
            </ul>
            """,
            "film_type": "color_change",
            "warranty_years": 3,
            "is_featured": True,
            "category_slug": "phim-doi-mau-xe",
            "brand_slug": "newnice"
        },
        {
            "name": "Newnice Architectural AR70",
            "short_description": "Phim cách nhiệt nhà kính - Trong suốt, tiết kiệm năng lượng",
            "description": """
            <h3>Newnice Architectural AR70 - Phim cách nhiệt nhà kính</h3>
            <p>Giải pháp cách nhiệt cho nhà ở và văn phòng, giúp tiết kiệm điện năng điều hòa.</p>
            <h4>Ưu điểm nổi bật:</h4>
            <ul>
                <li>Độ trong suốt cao - Không làm tối không gian</li>
                <li>Giảm nhiệt lên đến 60%</li>
                <li>Chặn 99% tia UV - Bảo vệ nội thất</li>
                <li>Tiết kiệm 30% chi phí điều hòa</li>
            </ul>
            """,
            "film_type": "ceramic",
            "vlt": 70,
            "uv_rejection": 99,
            "ir_rejection": 90,
            "heat_rejection": 55,
            "warranty_years": 5,
            "is_featured": True,
            "category_slug": "phim-cach-nhiet-nha-kinh",
            "brand_slug": "newnice"
        },
        # 3M products - Also available
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
            "is_featured": False,
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
            "is_featured": False,
            "category_slug": "phim-cach-nhiet-o-to",
            "brand_slug": "3m"
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
